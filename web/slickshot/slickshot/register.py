import os

from django.conf import settings

import csv


def job(job, selections):
    """
    Registers a new job in the platform (generates CSV and updates index).
    """
    # Generate CSV
    with open(os.path.join(settings.PLATFORM_HOME, "jobs", job, "{}.csv".format(job)), "wb") as fp:
        writer = csv.writer(fp)
        for selection in selections:
            writer.writerow([selection])

    # Update index
    with open(os.path.join(settings.PLATFORM_HOME, "jobs","index.txt"), "ab") as fp:
        fp.writelines([job + "\n"])
