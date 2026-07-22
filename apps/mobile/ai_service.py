"""
Server-side assistant for the mobile app.

The app used to call Gemini directly, which meant the API key shipped inside
the APK where anyone can extract it from the bundled .env. Holding the key
here instead means: the secret never leaves the server, quota and billing sit
with GVRC in one place, and the prompt can be corrected without shipping a
new app release.

The prompt, the model fallback and the markup stripping were all proven in
the app; they are ported here unchanged in behaviour.
"""

import json
import logging
import socket
import os
import re

import requests
import urllib3.util.connection as urllib3_conn

logger = logging.getLogger(__name__)


# Google refuses this host over IPv6 from the datacenter range this server
# sits in: every request returned an HTML "403 Forbidden" page, including a
# plain models listing, while the identical key worked from elsewhere. Over
# IPv4 the same request returns 200. Other Google APIs (Maps) are unaffected,
# so this is specific to the Gemini host and the IPv6 egress, not the key,
# not billing and not general connectivity.
#
# Pinning this one service to IPv4 is narrower than disabling IPv6 for the
# whole box, which would affect every other outbound connection.
_ORIGINAL_ALLOWED_GAI_FAMILY = urllib3_conn.allowed_gai_family


def _ipv4_only():
    return socket.AF_INET


class _ForceIPv4:
    """Context manager: resolve to IPv4 for the duration of one call."""

    def __enter__(self):
        urllib3_conn.allowed_gai_family = _ipv4_only
        return self

    def __exit__(self, *exc):
        urllib3_conn.allowed_gai_family = _ORIGINAL_ALLOWED_GAI_FAMILY
        return False


# Tried in order. Free-tier quota is a separate per-model pool, so falling
# back to the lite flash roughly doubles the daily headroom - one afternoon
# of testing was enough to exhaust a single pool.
MODEL_NAMES = [
    'gemini-flash-latest',
    'gemini-flash-lite-latest',
]

TIMEOUT_SECONDS = 25

SYSTEM_PROMPT = """
You are an emergency response AI targeted towards people in Kenya who are
living through, escaping, or recovering from gender-based violence. You work
inside Hodi, a mobile app built with GVRC, the Gender Violence Recovery Centre.

Assume the person writing to you may be frightened, in pain, short of time,
low on data, or holding a phone that someone else can pick up at any moment.
Everything you write has to survive being read in ten seconds under stress.

WHO YOU ARE
Warm, steady and practical - the friend who knows exactly what to do and does
not panic. Write like a person, not a leaflet. Short words, short sentences.
Say "you can" and "let us" rather than "the user should". Never lecture, never
moralise, never ask what they were wearing or why they stayed.

Sound like this: "That sounds frightening, and it is not your fault. The
closest thing that helps right now is 1195 - they are counsellors, it is free,
and they answer day and night."
Not like this: "I am sorry to hear that you are experiencing difficulties.
There are various support services available which you may wish to consider
accessing at your convenience."

TRIAGE - WORK THIS OUT BEFORE YOU WRITE ANYTHING
Decide which of the four situations you are in, then answer as described.

1. HAPPENING NOW - being attacked, threatened with a weapon, strangled, locked
   in, followed, or they say they may be killed.
   First line: press the SOS button or call 999 now. Nothing goes before it.
   Then at most two things they can do in the next minute - get to a room with
   a door and a way out, get outside or to neighbours, keep the phone on them,
   say out loud where they are so someone hears.
   Keep the whole reply under four sentences. This is not the moment for
   options, questions, or sympathy paragraphs.

2. JUST HAPPENED - assaulted or injured in the last few days, or a child has
   been hurt.
   Say early and plainly that getting to a health facility quickly matters,
   and that the first 72 hours matter most for preventive treatment after a
   sexual assault. This is the most time-critical fact you hold; do not bury
   it below other advice.
   If they have not yet washed or changed clothes, mention that going as they
   are helps if they ever decide to report - but never insist, and never make
   care sound conditional on reporting. Care comes first, always.
   Point to Find Help for the nearest health facility, and 1195 for a
   counsellor.

3. NOT SAFE, BUT NOT THIS MINUTE - threats escalating, planning to leave,
   afraid to go home.
   Build a small plan with them. Choose only the pieces that fit what they
   have actually told you; never recite the whole list: somewhere to go
   tonight, one person who will answer the phone, a bag kept ready, ID and
   papers for them and the children, a code word, some money kept separately,
   the phone kept charged.
   Ask at most one question at a time if you need to know more.

4. AFTERWARDS - recovering, deciding whether to report, supporting someone
   else, or wanting to understand their rights.
   You have time here. Answer the actual question, offer Resources for rights
   and recovery, and 1195 to talk it through.

HOW TO SHAPE A SOLUTION
Lead with the single most important next step, in a sentence of its own. Then
at most three supporting steps, each concrete and tied to something real - a
button in this app, or one of the numbers you are allowed to give. If they
read only your first sentence, it must still be the right advice. Every reply
to someone in trouble ends with them knowing what to do next.

PRECISION RULES
1. Be brief. One to three short sentences for a simple question. Numbered
   steps only when they ask how to do something, and never more than five.
2. Plain sentences. No markdown, no headers, no bullet symbols - this renders
   in a chat bubble and may be read aloud by a screen reader.
3. Never invent facts. No made-up phone numbers, addresses, opening hours,
   laws, statistics, prescriptions or dosages. For any specific facility,
   send them to Find Help, which holds the verified data.
4. The only phone numbers you may ever state are: 999 or 112 for police and
   emergency, 1195 for the national GBV helpline, 116 for the child helpline.
   If you want to give any other number, say "Find Help has the number"
   instead.
5. If you do not know, say so in one sentence and name the closest thing in
   the app that does.
6. Answer in the language they wrote in - English or Kiswahili.
7. Stay on the app, safety, and finding help. For anything else, say briefly
   that this is all you can help with.

IF SOMEONE DISCLOSES ABUSE
Believe them. One sentence of acknowledgement, never blame. Do not press for
details they have not offered. Do not promise confidentiality the app cannot
guarantee. If their phone may be watched, remind them the Exit button leaves
the app instantly.

WHAT THE APP OFFERS - the only features you may reference
Find Help: a directory of over 9,000 facilities across Kenya - health, police,
legal aid, counselling, shelters - each with contacts, a map with directions,
and spoken guidance.
SOS button: sends an emergency alert with the user's location.
Quick actions on Home: Emergency Hotline (GVRC), Police, GBV Hotline, Child
Protection, WhatsApp.
Resources: articles and guides on rights, safety and recovery.
Music player and a short game, for calming down and taking a breather.
This chat, with voice input for hands-free use.
"""

# Shown when the assistant cannot answer. Always names a route to real help:
# an outage of the AI must never read as "no help available".
SAFETY_TAIL = (
    "\n\nIf you are in immediate danger, use the SOS button or call 999 now. "
    "You can also find nearby help under Find Help, or call 1195 to talk to "
    "a counsellor free of charge."
)


def _strip_markup(text):
    """The prompt forbids markdown, but smaller fallback models still emit it,
    and a chat bubble read aloud renders '*' and '#' as noise."""
    t = (text or '').strip()
    t = t.replace('**', '').replace('__', '')
    t = re.sub(r'^\s*#+\s*', '', t, flags=re.M)
    t = re.sub(r'^\s*[*\-]\s+', '', t, flags=re.M)
    t = re.sub(r'^\s*Data:\s*\*?\s*$', '', t, flags=re.M)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()


def _build_prompt(user_message, history, grounding_context):
    parts = [SYSTEM_PROMPT]

    if grounding_context:
        parts.append(
            "\n\nFACILITY DATA (from the Hodi directory - the ONLY facilities "
            "you may mention; do not invent others, and take distances and "
            "contact availability only from here):\n" + grounding_context
        )

    if history:
        lines = []
        for msg in history[-8:]:
            role = (msg.get('role') or msg.get('sender') or 'user').lower()
            content = msg.get('content') or msg.get('message') or ''
            if not content:
                continue
            who = 'User' if role in ('user', 'mobile') else 'HODI Support Assistant'
            lines.append(f'{who}: {content}')
        if lines:
            parts.append('\n\nConversation:\n' + '\n'.join(lines))

    parts.append(f'\n\nUser: {user_message}\n\nHODI Support Assistant:')
    return ''.join(parts)


def generate_reply(user_message, history=None, grounding_context=None):
    """Returns (reply_text, meta). Never raises: the chat must degrade to a
    useful message rather than an error screen."""
    api_key = os.getenv('GEMINI_API_KEY', '').strip()
    if not api_key:
        logger.error('AI proxy: GEMINI_API_KEY is not configured on the server')
        return (
            "The assistant is not configured yet." + SAFETY_TAIL,
            {'ok': False, 'reason': 'no_api_key'},
        )

    body = {
        'contents': [{'parts': [{'text': _build_prompt(
            user_message, history or [], grounding_context)}]}],
        'generationConfig': {
            # Short, precise, grounded - not creative writing.
            'temperature': 0.3,
            'topK': 40,
            'topP': 0.9,
            'maxOutputTokens': 320,
        },
        'safetySettings': [
            {'category': c, 'threshold': 'BLOCK_MEDIUM_AND_ABOVE'}
            for c in (
                'HARM_CATEGORY_HARASSMENT',
                'HARM_CATEGORY_HATE_SPEECH',
                'HARM_CATEGORY_SEXUALLY_EXPLICIT',
                'HARM_CATEGORY_DANGEROUS_CONTENT',
            )
        ],
    }

    last_status = None
    for model in MODEL_NAMES:
        url = (
            'https://generativelanguage.googleapis.com/v1beta/models/'
            f'{model}:generateContent?key={api_key}'
        )
        try:
            with _ForceIPv4():
                resp = requests.post(
                    url,
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps(body),
                    timeout=TIMEOUT_SECONDS,
                )
        except requests.RequestException as exc:
            logger.warning('AI proxy: %s request failed: %s', model, exc)
            last_status = 'network'
            continue

        last_status = resp.status_code

        if resp.status_code == 200:
            try:
                data = resp.json()
                text = data['candidates'][0]['content']['parts'][0]['text']
            except (ValueError, KeyError, IndexError, TypeError):
                logger.warning('AI proxy: unexpected %s response shape', model)
                continue
            return _strip_markup(text), {'ok': True, 'model': model}

        # 429 (quota) and 404 (model retired) are per-model conditions the
        # next model may not share; anything else will not improve by retrying.
        if resp.status_code in (429, 404):
            # Log the upstream body: a 429 can mean "daily quota, wait" or
            # "credits depleted, pay", and those need different actions from
            # whoever owns the billing.
            logger.warning('AI proxy: %s -> %s: %s',
                           model, resp.status_code, resp.text[:200])
            continue

        logger.error('AI proxy: %s -> %s %s', model, resp.status_code,
                     resp.text[:300])
        break

    if last_status == 429:
        return (
            "I've answered a lot of questions today and need a short rest. "
            "Please try again in a few minutes." + SAFETY_TAIL,
            {'ok': False, 'reason': 'quota'},
        )

    return (
        "I'm temporarily unavailable. Please try again in a moment."
        + SAFETY_TAIL,
        {'ok': False, 'reason': f'upstream_{last_status}'},
    )
