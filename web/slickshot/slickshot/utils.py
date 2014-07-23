
import dropbox.client

from dropbox.rest import ErrorResponse

import redis

from django.conf import settings


def get_dropbox_client():
    """
    Returns a Dropbox client, already authenticated with the platform.
    """
    return dropbox.client.DropboxClient(settings.DROPBOX_TOKEN)


def get_redis_client():
    """
    Returns a Redis client, configured from settings.REDIS_URI.
    """
    return redis.from_url(settings.REDIS_URI)


def check_status(job):
    """
    Checks the status of a job, returns metadata if complete, False otherwise.
    """
    client = get_dropbox_client()

    try:
        return client.metadata(
            '/Video Automation Platform/jobs/{job}/{job}.png'.format(job=job))

    except ErrorResponse:
        return False


def share(job):
    """
    Shares the output for a job and returns the link.
    """
    client = get_dropbox_client()

    try:
        return client.share(
            '/Video Automation Platform/jobs/{job}/{job}.mov'.format(job=job))

    except ErrorResponse:
        return False
