"""
Generates a comprehensive, well-documented schema PDF for the GVRC Admin system.
Covers all tables, columns, data types, constraints, foreign keys, relationships,
and data engineering lifecycle guidance.
"""
import sqlite3
from weasyprint import HTML

DB_PATH = "/home/seven/Downloads/gvrc_admin-migration/db.sqlite3"
OUT_PATH = "/home/seven/Downloads/gvrc_admin-migration/GVRC_Database_Schema.pdf"

# Domain groupings for documentation
DOMAIN_GROUPS = {
    "Geography": ["counties", "constituencies", "wards"],
    "Facilities": [
        "facilities", "facility_contacts", "facility_coordinates",
        "facility_services", "facility_owners", "facility_gbv_categories",
        "facility_infrastructure",
    ],
    "Lookup / Reference": [
        "operational_statuses", "contact_types", "service_categories",
        "owner_types", "gbv_categories", "document_types",
        "infrastructure_types", "condition_statuses",
    ],
    "Users & Authentication": [
        "users", "user_profiles", "user_roles", "user_role_assignments",
        "permissions", "role_permissions",
        "auth_group", "auth_group_permissions", "auth_permission",
        "users_groups", "users_user_permissions",
    ],
    "Sessions & Tokens": [
        "user_sessions", "api_tokens", "authtoken_token", "custom_tokens",
    ],
    "Mobile": [
        "mobile_device_sessions", "mobile_device_usage",
        "contact_interactions",
    ],
    "Chat / Communications": [
        "emergency_chat_conversations", "emergency_chat_messages",
        "emergency_chat_notifications",
    ],
    "Documents": ["documents"],
    "Music / Media": ["music", "music_plays"],
    "Analytics & Audit": ["audit_trail", "application_settings"],
    "Django Internal": [
        "django_content_type", "django_migrations",
        "django_session", "django_admin_log", "sqlite_sequence",
    ],
}

TABLE_DESCRIPTIONS = {
    "counties": "Top-level administrative geographic division in Kenya (47 counties).",
    "constituencies": "Electoral/administrative sub-division within a county.",
    "wards": "Smallest administrative unit, nested within a constituency.",
    "facilities": "Core entity representing a health or GBV-support facility.",
    "facility_contacts": "Phone, email, or other contact details for a facility.",
    "facility_coordinates": "GPS coordinates (lat/lng) for map rendering and proximity search.",
    "facility_services": "Services offered by a facility with cost and availability info.",
    "facility_owners": "Ownership records (government, NGO, private, etc.).",
    "facility_gbv_categories": "M2M junction — which GBV service categories a facility supports.",
    "facility_infrastructure": "Physical infrastructure items (rooms, equipment) at a facility.",
    "operational_statuses": "Lookup — operational state of a facility (open, closed, etc.).",
    "contact_types": "Lookup — type of contact (phone, email, WhatsApp, etc.).",
    "service_categories": "Lookup — category of service (medical, legal, shelter, etc.).",
    "owner_types": "Lookup — ownership category (public, private, faith-based, etc.).",
    "gbv_categories": "Lookup — types of Gender-Based Violence services.",
    "document_types": "Lookup — allowed document types with file-extension rules.",
    "infrastructure_types": "Lookup — categories of physical infrastructure.",
    "condition_statuses": "Lookup — condition state of infrastructure items.",
    "users": "System users (admins, facility staff). Extends Django AbstractBaseUser.",
    "user_profiles": "Extended profile info (bio, department, job title, avatar).",
    "user_roles": "Role definitions (admin, viewer, editor, etc.) for RBAC.",
    "user_role_assignments": "M2M junction assigning roles to users with optional expiry.",
    "permissions": "Granular resource/action permission definitions.",
    "role_permissions": "M2M junction granting permissions to roles.",
    "auth_group": "Django built-in groups.",
    "auth_group_permissions": "Django M2M: group → permission.",
    "auth_permission": "Django built-in permission codenames.",
    "users_groups": "Django M2M: user → group.",
    "users_user_permissions": "Django M2M: user → direct permission.",
    "user_sessions": "Active browser/API sessions with location and expiry.",
    "api_tokens": "Named API tokens for programmatic access, scoped per user.",
    "authtoken_token": "DRF TokenAuthentication tokens.",
    "custom_tokens": "Custom token scheme mirroring DRF tokens.",
    "mobile_device_sessions": "Anonymous mobile-app device sessions identified by device_id.",
    "mobile_device_usage": "Feature-level analytics per device session.",
    "contact_interactions": "Tracks when a mobile user taps a facility contact (click analytics).",
    "emergency_chat_conversations": "Chat threads between mobile users and admin staff.",
    "emergency_chat_messages": "Individual messages within a chat conversation.",
    "emergency_chat_notifications": "Push/in-app notifications tied to chat events.",
    "documents": "Uploaded documents (PDFs, images) linked to facilities/GBV categories.",
    "music": "Audio tracks available for in-app music playback.",
    "music_plays": "Audit log of music plays per user session.",
    "audit_trail": "Immutable audit log for all significant data changes (who/what/when).",
    "application_settings": "Singleton table storing site-wide branding and configuration.",
    "django_content_type": "Django internal — content-type registry for generic relations.",
    "django_migrations": "Django internal — applied migration history.",
    "django_session": "Django internal — server-side session store.",
    "django_admin_log": "Django admin action log.",
    "sqlite_sequence": "SQLite internal — autoincrement counters.",
}

TYPE_NOTES = {
    "INTEGER": "64-bit signed integer",
    "bigint": "64-bit signed integer (Django BigIntegerField)",
    "smallint unsigned": "Small unsigned integer",
    "varchar": "Variable-length text (max length in parentheses)",
    "TEXT": "Unbounded text / JSON blob",
    "bool": "Boolean (stored as 0/1 in SQLite)",
    "datetime": "ISO 8601 timestamp with timezone (UTC)",
    "date": "Calendar date (YYYY-MM-DD)",
    "decimal": "Decimal number (lat/lng precision)",
    "char": "Fixed-length text (e.g. IP addresses)",
}


def get_schema(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [t[0] for t in c.fetchall()]
    schema = {}
    for table in tables:
        c.execute("PRAGMA table_info(" + table + ")")
        cols = c.fetchall()
        c.execute("PRAGMA foreign_key_list(" + table + ")")
        fks = {row[3]: (row[2], row[4]) for row in c.fetchall()}
        c.execute("PRAGMA index_list(" + table + ")")
        idxs = []
        for idx in c.fetchall():
            c.execute("PRAGMA index_info(" + idx[1] + ")")
            idx_cols = [i[2] for i in c.fetchall()]
            idxs.append({"name": idx[1], "unique": bool(idx[2]), "cols": idx_cols})
        schema[table] = {"cols": cols, "fks": fks, "idxs": idxs}
    conn.close()
    return schema


def col_html(col, fks):
    cid, name, dtype, notnull, dflt, pk = col
    badges = []
    if pk:
        badges.append('<span class="badge pk">PK</span>')
    if name in fks:
        ref_table, ref_col = fks[name]
        badges.append(f'<span class="badge fk">FK → {ref_table}.{ref_col}</span>')
    if notnull and not pk:
        badges.append('<span class="badge nn">NOT NULL</span>')
    if dflt is not None:
        badges.append(f'<span class="badge df">DEFAULT {dflt}</span>')
    badge_str = " ".join(badges)
    base_type = dtype.split("(")[0].upper()
    type_hint = TYPE_NOTES.get(base_type, TYPE_NOTES.get(dtype.split("(")[0], ""))
    type_tip = f'<span class="type-hint" title="{type_hint}">{dtype}</span>' if type_hint else f'<span class="type-hint">{dtype}</span>'
    return f"""
    <tr>
      <td class="col-name">{name}</td>
      <td>{type_tip}</td>
      <td>{badge_str}</td>
    </tr>"""


def table_section(name, info):
    cols = info["cols"]
    fks = info["fks"]
    idxs = info["idxs"]
    desc = TABLE_DESCRIPTIONS.get(name, "")
    desc_html = f'<p class="table-desc">{desc}</p>' if desc else ""
    rows = "".join(col_html(c, fks) for c in cols)
    idx_html = ""
    if idxs:
        idx_rows = ""
        for idx in idxs:
            u = "UNIQUE " if idx["unique"] else ""
            idx_rows += f'<tr><td>{idx["name"]}</td><td>{u}INDEX</td><td>{", ".join(idx["cols"])}</td></tr>'
        idx_html = f"""
        <h4 class="idx-title">Indexes</h4>
        <table class="idx-table">
          <tr><th>Name</th><th>Type</th><th>Columns</th></tr>
          {idx_rows}
        </table>"""
    return f"""
    <div class="table-block" id="tbl-{name}">
      <h3 class="table-name">{name}</h3>
      {desc_html}
      <table class="col-table">
        <thead><tr><th>Column</th><th>Type</th><th>Constraints</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      {idx_html}
    </div>"""


def build_html(schema):
    all_grouped = set()
    domain_sections = ""
    toc_items = ""

    for domain, tables in DOMAIN_GROUPS.items():
        domain_sections += f'<h2 class="domain-title">{domain}</h2>\n'
        toc_items += f'<li class="toc-domain"><strong>{domain}</strong><ul>'
        for t in tables:
            if t in schema:
                domain_sections += table_section(t, schema[t])
                toc_items += f'<li><a href="#tbl-{t}">{t}</a></li>'
                all_grouped.add(t)
        toc_items += "</ul></li>"

    ungrouped = [t for t in schema if t not in all_grouped]
    if ungrouped:
        domain_sections += '<h2 class="domain-title">Other</h2>\n'
        toc_items += '<li class="toc-domain"><strong>Other</strong><ul>'
        for t in ungrouped:
            domain_sections += table_section(t, schema[t])
            toc_items += f'<li><a href="#tbl-{t}">{t}</a></li>'
        toc_items += "</ul></li>"

    table_count = len(schema)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>GVRC Admin — Database Schema</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 15mm 18mm 15mm;
    @top-center {{ content: "GVRC Admin — Database Schema"; font-size: 9pt; color: #666; }}
    @bottom-right {{ content: "Page " counter(page) " of " counter(pages); font-size: 9pt; color: #666; }}
  }}
  body {{ font-family: "DejaVu Sans", Arial, sans-serif; font-size: 9pt; color: #1a1a2e; margin: 0; }}
  h1 {{ font-size: 22pt; color: #16213e; margin-bottom: 4pt; }}
  h2.domain-title {{ font-size: 14pt; color: #0f3460; border-bottom: 2px solid #0f3460; margin-top: 24pt; margin-bottom: 8pt; padding-bottom: 3pt; page-break-before: always; }}
  h2.domain-title:first-of-type {{ page-break-before: avoid; }}
  h3.table-name {{ font-size: 11pt; color: #e94560; margin: 16pt 0 4pt 0; }}
  h4.idx-title {{ font-size: 9pt; color: #555; margin: 8pt 0 3pt 0; }}
  .subtitle {{ color: #444; font-size: 11pt; margin-bottom: 2pt; }}
  .meta {{ color: #777; font-size: 8.5pt; margin-bottom: 14pt; }}
  .table-desc {{ color: #444; margin: 0 0 6pt 0; font-style: italic; }}
  .table-block {{ margin-bottom: 20pt; page-break-inside: avoid; }}
  table.col-table {{ width: 100%; border-collapse: collapse; margin-bottom: 4pt; }}
  table.col-table thead tr {{ background: #0f3460; color: white; }}
  table.col-table thead th {{ padding: 4pt 6pt; text-align: left; font-size: 8.5pt; }}
  table.col-table tbody tr:nth-child(even) {{ background: #f4f7fb; }}
  table.col-table td {{ padding: 3pt 6pt; border-bottom: 1px solid #dde3ed; vertical-align: top; }}
  .col-name {{ font-weight: bold; font-family: "DejaVu Sans Mono", monospace; font-size: 8pt; }}
  .type-hint {{ font-family: "DejaVu Sans Mono", monospace; font-size: 7.5pt; color: #0057a8; }}
  .badge {{ display: inline-block; padding: 1pt 4pt; border-radius: 3pt; font-size: 7pt; font-weight: bold; margin-right: 2pt; }}
  .badge.pk {{ background: #e94560; color: white; }}
  .badge.fk {{ background: #0f3460; color: white; font-weight: normal; font-size: 6.5pt; }}
  .badge.nn {{ background: #f0a500; color: white; }}
  .badge.df {{ background: #4caf50; color: white; font-weight: normal; }}
  table.idx-table {{ width: 100%; border-collapse: collapse; font-size: 7.5pt; }}
  table.idx-table th {{ background: #e8ecf4; padding: 2pt 5pt; text-align: left; }}
  table.idx-table td {{ padding: 2pt 5pt; border-bottom: 1px solid #dde3ed; font-family: "DejaVu Sans Mono", monospace; }}
  .cover {{ margin-bottom: 20pt; }}
  .toc {{ column-count: 2; column-gap: 16pt; margin: 14pt 0 20pt 0; }}
  .toc ul {{ list-style: none; margin: 0; padding: 0; }}
  .toc li {{ margin: 1pt 0; }}
  .toc a {{ color: #0f3460; text-decoration: none; font-size: 8pt; }}
  .toc-domain {{ margin-top: 6pt; font-size: 8.5pt; }}
  .toc-domain > strong {{ color: #0f3460; }}
  .section-header {{ background: #eef2fb; padding: 10pt 12pt; border-left: 4px solid #0f3460; margin-bottom: 12pt; }}
  .erd-note {{ background: #fff8e1; border: 1px solid #ffe082; padding: 8pt 12pt; margin: 10pt 0; font-size: 8pt; border-radius: 3pt; }}
  .lifecycle-section {{ margin: 14pt 0; }}
  .lifecycle-section h3 {{ color: #0f3460; font-size: 11pt; }}
  .lifecycle-table {{ width: 100%; border-collapse: collapse; font-size: 8pt; }}
  .lifecycle-table th {{ background: #0f3460; color: white; padding: 4pt 8pt; text-align: left; }}
  .lifecycle-table td {{ padding: 4pt 8pt; border-bottom: 1px solid #dde; vertical-align: top; }}
  .lifecycle-table tr:nth-child(even) {{ background: #f4f7fb; }}
</style>
</head>
<body>

<!-- ===================== COVER ===================== -->
<div class="cover">
  <h1>GVRC Admin System</h1>
  <p class="subtitle">Complete Database Schema Reference</p>
  <p class="subtitle">Data Engineering & Extraction Guide</p>
  <p class="meta">Generated: 2026-04-20 &nbsp;|&nbsp; Database: SQLite (production-equivalent) &nbsp;|&nbsp; Tables: {table_count} &nbsp;|&nbsp; System: Hodi GBV Resource Centre</p>
  <hr/>
</div>

<!-- ===================== OVERVIEW ===================== -->
<div class="section-header">
  <strong>System Purpose</strong><br/>
  The GVRC (Gender-Based Violence Resource Centre) Admin system manages health and support facilities across Kenya.
  It tracks geographical coverage (county → constituency → ward → facility), services offered, contact information,
  document repositories, user authentication/RBAC, mobile-app sessions, emergency chat, music media, and a full audit trail.
</div>

<div class="erd-note">
  <strong>Entity Relationship Summary:</strong>
  County &#8594; Constituency &#8594; Ward &#8594; Facility &#8594; (Contacts, Coordinates, Services, Owners, GBV Categories, Infrastructure, Documents)<br/>
  User &#8594; (Profile, Roles &#8594; Permissions, Sessions &#8594; API Tokens)<br/>
  MobileDeviceSession &#8594; (Usage, ContactInteractions, ChatConversations &#8594; Messages &#8594; Notifications)
</div>

<!-- ===================== DATA ENGINEERING LIFECYCLE ===================== -->
<h2 class="domain-title" style="page-break-before:avoid;">Data Engineering Lifecycle Guide</h2>

<div class="lifecycle-section">
  <h3>1. Data Extraction Guidance</h3>
  <table class="lifecycle-table">
    <tr><th>Domain</th><th>Primary Tables</th><th>Join Keys</th><th>Extraction Notes</th></tr>
    <tr>
      <td>Facility Directory</td>
      <td>facilities, facility_contacts, facility_coordinates, facility_services, facility_owners</td>
      <td>facility_id</td>
      <td>Always join ward → constituency → county for full geography. Filter is_active=1. Use collection_date on coordinates for freshness checks.</td>
    </tr>
    <tr>
      <td>GBV Services Map</td>
      <td>facility_gbv_categories, gbv_categories, facilities, facility_coordinates</td>
      <td>facility_id, gbv_category_id</td>
      <td>Pivot gbv_category_id for wide-format export. Exclude inactive facilities.</td>
    </tr>
    <tr>
      <td>User Activity</td>
      <td>user_sessions, api_tokens, users, user_profiles</td>
      <td>user_id, session_id</td>
      <td>Use last_activity_at for session recency. expires_at for active filter. Join user_role_assignments for role context.</td>
    </tr>
    <tr>
      <td>Mobile Analytics</td>
      <td>mobile_device_sessions, mobile_device_usage, contact_interactions</td>
      <td>device_id</td>
      <td>device_id is the anonymous identifier — not linkable to users by design. Aggregate by feature_category for funnel analysis.</td>
    </tr>
    <tr>
      <td>Contact Engagement</td>
      <td>contact_interactions, facility_contacts, facilities</td>
      <td>contact_id, device_id</td>
      <td>interaction_type distinguishes calls vs. messages. is_helpful captures outcome signal. Use created_at for time-series.</td>
    </tr>
    <tr>
      <td>Audit / Compliance</td>
      <td>audit_trail, users, user_sessions</td>
      <td>session_id, record_id + table_name</td>
      <td>old_values/new_values/changed_fields are JSON blobs — parse with json_extract. Filter by action_type (INSERT/UPDATE/DELETE) and severity_level.</td>
    </tr>
    <tr>
      <td>Chat Operations</td>
      <td>emergency_chat_conversations, emergency_chat_messages, emergency_chat_notifications</td>
      <td>conversation_id, message_id</td>
      <td>status on conversations: open/closed/escalated. priority field for triage. unread counts for SLA reporting.</td>
    </tr>
    <tr>
      <td>Documents</td>
      <td>documents, document_types, gbv_categories, users</td>
      <td>document_id, document_type_id, gbv_category</td>
      <td>file_url / file fields point to object storage. external_url for linked resources. Filter is_active=1 and is_public for public portal.</td>
    </tr>
  </table>
</div>

<div class="lifecycle-section">
  <h3>2. Data Quality Rules</h3>
  <table class="lifecycle-table">
    <tr><th>Rule</th><th>Table / Column</th><th>Check</th></tr>
    <tr><td>No orphaned facilities</td><td>facilities.ward_id</td><td>Every ward_id must exist in wards</td></tr>
    <tr><td>Coordinate bounds (Kenya)</td><td>facility_coordinates.latitude/longitude</td><td>Lat: -5.0 to 5.0 | Lng: 33.9 to 42.0</td></tr>
    <tr><td>Unique registration</td><td>facilities.registration_number</td><td>Must be unique and non-empty</td></tr>
    <tr><td>Active primary contact</td><td>facility_contacts.is_primary</td><td>Each facility should have exactly one is_primary=1 contact</td></tr>
    <tr><td>Session expiry integrity</td><td>user_sessions.expires_at</td><td>expires_at must be &gt; created_at</td></tr>
    <tr><td>Audit completeness</td><td>audit_trail.old_values / new_values</td><td>Both fields must be valid JSON for UPDATE actions</td></tr>
    <tr><td>Geography hierarchy</td><td>wards → constituencies → counties</td><td>No ward without a constituency; no constituency without a county</td></tr>
  </table>
</div>

<div class="lifecycle-section">
  <h3>3. Recommended Extraction Queries</h3>
  <table class="lifecycle-table">
    <tr><th>Use Case</th><th>SQL Pattern</th></tr>
    <tr>
      <td>Full facility export with geography</td>
      <td style="font-family:monospace;font-size:7pt;">SELECT f.*, w.ward_name, c.constituency_name, co.county_name FROM facilities f JOIN wards w ON f.ward_id=w.ward_id JOIN constituencies c ON w.constituency_id=c.constituency_id JOIN counties co ON c.county_id=co.county_id WHERE f.is_active=1</td>
    </tr>
    <tr>
      <td>GBV service pivot per facility</td>
      <td style="font-family:monospace;font-size:7pt;">SELECT f.facility_id, f.facility_name, GROUP_CONCAT(g.category_name, ', ') AS gbv_services FROM facilities f JOIN facility_gbv_categories fgc ON f.facility_id=fgc.facility_id JOIN gbv_categories g ON fgc.gbv_category_id=g.gbv_category_id GROUP BY f.facility_id</td>
    </tr>
    <tr>
      <td>Daily contact interaction counts</td>
      <td style="font-family:monospace;font-size:7pt;">SELECT DATE(created_at) AS day, interaction_type, COUNT(*) AS n, SUM(is_helpful) AS helpful FROM contact_interactions GROUP BY 1,2 ORDER BY 1 DESC</td>
    </tr>
    <tr>
      <td>Active users last 30 days</td>
      <td style="font-family:monospace;font-size:7pt;">SELECT u.user_id, u.full_name, u.email, MAX(s.last_activity_at) AS last_seen FROM users u JOIN user_sessions s ON u.user_id=s.user_id WHERE s.last_activity_at &gt; datetime('now','-30 days') GROUP BY u.user_id</td>
    </tr>
    <tr>
      <td>Audit trail changes by table</td>
      <td style="font-family:monospace;font-size:7pt;">SELECT table_name, action_type, COUNT(*) AS changes, DATE(created_at) AS day FROM audit_trail GROUP BY 1,2,4 ORDER BY day DESC</td>
    </tr>
  </table>
</div>

<div class="lifecycle-section">
  <h3>4. ETL / Pipeline Design Notes</h3>
  <ul style="font-size:8pt; line-height:1.7;">
    <li><strong>Incremental extraction:</strong> All main tables have <code>created_at</code> and <code>updated_at</code>. Use <code>updated_at &gt; last_run_watermark</code> for CDC (Change Data Capture) loads.</li>
    <li><strong>Soft deletes:</strong> Most tables use <code>is_active</code> (bool) rather than hard deletes. Always filter appropriately for operational vs. historical data marts.</li>
    <li><strong>Audit trail as CDC source:</strong> <code>audit_trail</code> is an append-only log. It can be used as an alternative CDC stream — parse <code>changed_fields</code> (JSON array) to identify which columns changed.</li>
    <li><strong>JSON blob columns:</strong> <code>audit_trail.old_values</code>, <code>audit_trail.new_values</code>, <code>mobile_device_usage.additional_data</code>, <code>user_sessions.session_data</code>, and <code>user_profiles.notification_preferences</code> store JSON. Flatten these in transformation layer.</li>
    <li><strong>Geography lookup tables</strong> (counties, constituencies, wards) are largely static — cache aggressively, refresh weekly.</li>
    <li><strong>Mobile anonymity:</strong> <code>mobile_device_sessions.device_id</code> is a random UUID — there is no user_id linkage by design (privacy). Do not attempt to join with user tables.</li>
    <li><strong>Token tables</strong> (api_tokens, authtoken_token, custom_tokens) contain sensitive hashes — mask or exclude from analytical exports. Load to secure schema only.</li>
  </ul>
</div>

<!-- ===================== TABLE OF CONTENTS ===================== -->
<h2 class="domain-title">Table of Contents</h2>
<div class="toc">
  <ul>{toc_items}</ul>
</div>

<!-- ===================== SCHEMA SECTIONS ===================== -->
{domain_sections}

</body>
</html>"""
    return html


def main():
    print("Extracting schema from database...")
    schema = get_schema(DB_PATH)
    print(f"Found {len(schema)} tables.")
    print("Building HTML document...")
    html = build_html(schema)
    print("Rendering PDF (this may take a moment)...")
    HTML(string=html, base_url="/").write_pdf(OUT_PATH)
    print(f"PDF written to: {OUT_PATH}")


if __name__ == "__main__":
    main()
