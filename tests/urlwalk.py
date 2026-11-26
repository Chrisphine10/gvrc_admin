"""
Enumerate every URL pattern the project routes, generically.

Each leaf pattern becomes a ``Route`` with a dotted name (namespace chain plus
the pattern name), a printable template and the list of URL parameters it
needs. ``Route.build(values)`` turns it into a concrete path using Django's
own reverse machinery (``regex_helper.normalize``), so path() and re_path()
routes - including DRF router patterns - are handled the same way.

New URLs (for example the map-config endpoint or the SMS app being added)
are picked up automatically; nothing here lists URLs by hand.
"""

from dataclasses import dataclass, field

from django.urls import URLPattern, URLResolver, get_resolver
from django.utils.regex_helper import normalize


@dataclass
class Route:
    name: str            # e.g. "facilities:facility_detail" or "<unnamed>"
    regex: str           # concatenated regex
    template: str        # e.g. "facilities/%(facility_id)s/"
    params: list = field(default_factory=list)
    callback: object = None

    @property
    def id(self):
        return f"{self.name} /{self.template}".replace("%(", "<").replace(")s", ">")

    def build(self, values):
        return "/" + (self.template % {p: values[p] for p in self.params})


def _strip(pattern):
    return pattern[1:] if pattern.startswith("^") else pattern


def iter_routes(resolver=None, prefix="", namespaces=()):
    resolver = resolver or get_resolver()
    for entry in resolver.url_patterns:
        regex = _strip(entry.pattern.regex.pattern)
        if isinstance(entry, URLResolver):
            ns = namespaces + ((entry.namespace,) if entry.namespace else ())
            yield from iter_routes(entry, prefix + regex, ns)
        elif isinstance(entry, URLPattern):
            full = prefix + regex
            possibilities = normalize("^" + full)
            if not possibilities:
                continue
            template, params = possibilities[0]
            name = entry.name or "<unnamed>"
            if namespaces:
                name = ":".join(namespaces) + ":" + name
            yield Route(name=name, regex=full, template=template,
                        params=list(params), callback=entry.callback)


def all_routes():
    """Unique routes, minus DRF's ``.json`` format-suffix duplicates."""
    seen = set()
    out = []
    for r in iter_routes():
        if "format" in r.params and r.name != "schema-json":
            continue  # DRF format_suffix_patterns twin of a route we keep
        if r.template.startswith("static/") or r.template.startswith("media/"):
            continue
        key = r.template
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out
