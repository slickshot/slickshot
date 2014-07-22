import json

import uuid

from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from rest_framework.renderers import JSONRenderer

from . import register
from . import utils


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def index(request):
    return HttpResponseForbidden("Forbidden")


def generate_uuid(request):
    return HttpResponse(uuid.uuid4().hex)


@csrf_exempt
@require_http_methods(["POST"])
def shoot(request):
    """
    Given a valid request, registers a new job in the platform.
    """
    # Get data and register a new job
    try:
        data = json.load(request)
        register.job(
            data["job"],
            [selection.split("/")[-1] for selection in data["selections"]])
    except:
        return HttpResponseBadRequest("Bad request")

    return HttpResponse("Accepted", status=202)


def status(request):
    """
    Checks status of a job.
    """
    try:
        job = request.GET["job"]

    except:
        return HttpResponseBadRequest("Bad request")

    metadata = utils.check_status(job)
    if metadata:
        return JSONResponse(metadata)

    else:
        return HttpResponseNotFound("Not found")


@csrf_exempt
@require_http_methods(["POST"])
def share(request):
    """
    Shares the output of a job.
    """
    try:
        job = json.load(request)

    except:
        return HttpResponseBadRequest("Bad request")

    metadata = utils.share(job)
    if metadata:
        return JSONResponse(metadata)

    else:
        return HttpResponseNotFound("Not found")
