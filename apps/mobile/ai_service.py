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
import os
import re

import requests

logger = logging.getLogger(__name__)

# Tried in order. Free-tier quota is a separate per-model pool, so falling
# back to the lite flash roughly doubles the daily headroom - one afternoon
# of testing was enough to exhaust a single pool.
MODEL_NAMES = [
    'gemini-flash-latest',
    'gemini-flash-lite-latest',
]

TIMEOUT_SECONDS = 25

SYSTEM_PROMPT = """
You are Hodi's support assistant. Hodi is a Kenyan mobile app that helps
people affected by gender-based violence (GBV) find help safely.

WHAT THE APP OFFERS (the only features you may reference):
- Find Help: a directory of over 9,000 facilities across Kenya (health,
  police, legal aid, counselling, shelters). Each entry can show contacts,
  a map with directions, and spoken guidance.
- SOS button: sends an emergency alert with the user's location.
- Quick actions on Home: Emergency Hotline (GVRC), Police, GBV Hotline,
  Child Protection, WhatsApp.
- Resources: articles and guides about rights, safety, and recovery.
- Music player and a small game: for calming and taking a breather.
- This chat, with voice input for hands-free use.

HOW TO ANSWER - PRECISION RULES:
1. Be brief. 1-3 short sentences for a simple question. Only give numbered
   steps when the user asks how to do something, and at most 5 steps.
2. Plain sentences only. No markdown, no headers, no bullet symbols - this
   renders in a chat bubble and may be read aloud by a screen reader.
3. Never invent facts. No made-up phone numbers, addresses, opening hours,
   laws, statistics, or medical advice. For any specific facility, direct
   the user to Find Help, which holds the verified data.
4. The only phone numbers you may state are: 999 or 112 (Kenya police and
   emergency), 1195 (national GBV toll-free helpline), 116 (child helpline).
5. If you do not know, say so in one sentence and point to the closest
   feature in the app that can help.
6. Answer in the language the user wrote - English or Kiswahili.
7. Stay on topic: the app, safety, and finding help. For anything else,
   say briefly that you can only help with Hodi and staying safe.

IF SOMEONE DISCLOSES DANGER OR ABUSE:
- Believe them. One sentence of acknowledgement, never blame, never lecture.
- If they are in immediate danger: tell them to use the SOS button or call
  999 now. This comes first, before anything else.
- Otherwise point to the specific help that fits: Find Help for nearby
  facilities, 1195 to talk to a trained counsellor, the GBV Hotline quick
  action on the Home screen.
- Do not press for details they have not offered. Do not promise
  confidentiality the app cannot guarantee. If their phone may be watched,
  remind them the Exit button leaves the app instantly.
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
            logger.info('AI proxy: %s -> %s, trying next model',
                        model, resp.status_code)
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
