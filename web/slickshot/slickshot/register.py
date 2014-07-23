import os

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from django.conf import settings

import csv

from . import utils


def job(job, selections):
    """
    Registers a new job in the platform (generates CSV and updates index).
    """
    # Get a Dropbox client, so we can sync the job info there for processing by AE
    dropbox = utils.get_dropbox_client()

    # Get a Redis client, for this is where we save our jobs
    redis = utils.get_redis_client()

    # Save the job in redis
    redis.rpush("jobs", job)

    # Generate CSV
    fp = StringIO.StringIO()
    writer = csv.writer(fp)
    for selection in selections:
        writer.writerow([selection])

    # Upload CSV to Dropbox
    dropbox.put_file(
        os.path.join(
            settings.PLATFORM_HOME, "jobs", job, "{}.csv".format(job)
        ), fp, overwrite=True)
    fp.close()

    # Generate index
    jobs = redis.lrange("jobs", 0, -1)
    fp = StringIO.StringIO()
    for job in jobs:
        fp.write("{}\n".format(job))

    # TODO
    # Beware race conditions here!

    # Upload index to Dropbox
    dropbox.put_file(
        os.path.join(
            settings.PLATFORM_HOME, "jobs", "index.txt"
        ), fp, overwrite=True)
    fp.close()
