"""
Static files storage for production.

WhiteNoise's CompressedManifestStaticFilesStorage gives every file a
content-hashed name (so browsers can cache it for a year) and serves
compressed copies. Out of the box it is unforgiving in two ways that have
bitten this project:

* ``collectstatic`` aborts if any CSS file references a file that does not
  exist. The Argon theme CSS points at twelve calendar header images that were
  never shipped, so the deploy's collectstatic failed outright.
* At runtime, ``{% static %}`` on a path missing from the manifest raises
  ValueError, turning a single typo into a 500 page.

This subclass leaves an unresolvable CSS reference as it was (logging a
warning) and, with ``manifest_strict = False``, falls back to the unhashed
name at runtime. Everything that does exist is still hashed and compressed.
"""

import logging

from whitenoise.storage import CompressedManifestStaticFilesStorage

logger = logging.getLogger(__name__)


class HodiStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False

    def url_converter(self, name, hashed_files, *args, **kwargs):
        convert = super().url_converter(name, hashed_files, *args, **kwargs)

        def tolerant(matchobj):
            try:
                return convert(matchobj)
            except ValueError as exc:
                logger.warning("Static file %s: leaving reference unhashed (%s)", name, exc)
                return matchobj.group(0)

        return tolerant
