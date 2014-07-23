import os

from django.conf import settings

import csv


def job(job, selections):
    """
    Registers a new job in the platform (generates CSV and updates index).
    """

    # TODO
    # Generate CSV and upload directly to Dropbox using the REST API
    # Be sure to use overwrite mode.

    # TODO
    # Append job to Redis 'jobs' list
    # Just set it as the last element so it's as quick as possible (O(1))

    # TODO
    # Generate new index.txt from Redis 'jobs' list
    # Upload to Dropbox using the REST API
    # Be sure to use overwrite mode.

    # Generate CSV
    with open(os.path.join(settings.PLATFORM_HOME, "jobs", job, "{}.csv".format(job)), "wb") as fp:
        writer = csv.writer(fp)
        for selection in selections:
            writer.writerow([selection])

    # Update index
    with open(os.path.join(settings.PLATFORM_HOME, "jobs","index.txt"), "ab") as fp:
        fp.writelines([job + "\n"])
