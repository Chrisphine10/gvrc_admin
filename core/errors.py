"""One place for what users see when something goes wrong.

* The mobile app and other API clients always get JSON: ``{"error": "..."}``
  (plus DRF's usual ``detail`` / field errors where they exist), never an HTML
  error page they cannot read.
* People in a browser get the branded 403/404/500 pages.
* The real exception is logged with its traceback; its text is never sent to
  the client, because it can reveal internals (paths, SQL, settings).
"""

import logging

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger("hodi.errors")

API_PREFIXES = ("/api/", "/mobile/")
SERVER_ERROR_MESSAGE = "Something went wrong on our side. Please try again in a moment."


def wants_json(request) -> bool:
    path = getattr(request, "path", "") or ""
    accept = request.META.get("HTTP_ACCEPT", "") if hasattr(request, "META") else ""
    return path.startswith(API_PREFIXES) or ("application/json" in accept and "text/html" not in accept)


def api_exception_handler(exc, context):
    """DRF EXCEPTION_HANDLER: known API errors keep DRF's shape plus an
    ``error`` string; anything unexpected becomes a logged 500 with a calm
    message instead of an HTML traceback page."""
    response = drf_exception_handler(exc, context)
    if response is None:
        view = context.get("view")
        logger.exception("Unhandled API error in %s", view.__class__.__name__ if view else "?", exc_info=exc)
        return Response({"error": SERVER_ERROR_MESSAGE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    data = response.data
    if isinstance(data, dict) and "error" not in data:
        detail = data.get("detail")
        if detail is not None:
            data["error"] = str(detail)
        elif data:
            data["error"] = "Please check the details you sent and try again."
    elif isinstance(data, list):
        response.data = {"error": " ".join(str(x) for x in data) or "Request could not be completed.", "detail": data}
    return response


def _page(request, template, status_code, json_message):
    if wants_json(request):
        return JsonResponse({"error": json_message}, status=status_code)
    try:
        return render(request, template, status=status_code)
    except Exception:  # the error page itself must never fail
        logger.exception("Could not render %s", template)
        return HttpResponse(f"<h1>{status_code}</h1><p>{json_message}</p>", status=status_code)


def bad_request(request, exception=None):
    return _page(request, "home/page-404.html", 400, "Bad request.")


def permission_denied(request, exception=None):
    return _page(request, "home/page-403.html", 403, "You do not have permission to do that.")


def page_not_found(request, exception=None):
    return _page(request, "home/page-404.html", 404, "Not found.")


def server_error(request):
    if wants_json(request):
        return JsonResponse({"error": SERVER_ERROR_MESSAGE}, status=500)
    try:
        # No context processors: the database may be what failed.
        from django.template.loader import get_template
        return HttpResponse(get_template("home/page-500.html").render({}), status=500)
    except Exception:
        logger.exception("Could not render the 500 page")
        return HttpResponse(f"<h1>Server error</h1><p>{SERVER_ERROR_MESSAGE}</p>", status=500)
