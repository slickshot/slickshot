import os

from fabric.api import local


BASE_DIR = os.path.sep.join((os.path.dirname(__file__), ''))


def shell():
    """
    Runs the Django development server.
    """
    environ = "DROPBOX_TOKEN={}".format(os.environ["DROPBOX_TOKEN"])
    local(environ + " " + os.path.join(BASE_DIR, "web/slickshot/manage.py") + " shell")


def runserver():
    """
    Runs the Django development server.
    """
    environ = "DROPBOX_TOKEN={}".format(os.environ["DROPBOX_TOKEN"])
    local(environ + " " + os.path.join(BASE_DIR, "web/slickshot/manage.py") + " runserver")


def ngrok():
    """
    Runs ngrok.
    """
    local("ngrok -subdomain=slickshot 8000")
