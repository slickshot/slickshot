import dropbox.client
from dropbox.rest import ErrorResponse

from django.conf import settings


def get_dropbox_client():
    """
    Returns a Dropbox client, already authenticated with the platform.
    """
    return dropbox.client.DropboxClient(settings.DROPBOX_TOKEN)



def check_status(job):
    """
    Checks the status of a job, returns metadata if complete, False otherwise.
    """
    client = get_dropbox_client()

    try:
        return client.metadata(
            '/Video Automation Platform/jobs/{job}/{job}.mov'.format(job=job))

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
