#!/usr/bin/env python
"""
Generates CSV in 'SlickShot format'.
"""

import os
import sys
import csv


PLATFORM_HOME = os.path.realpath(
    os.path.join(os.path.dirname(__file__), "..", "platform")
)


def collect_assets(job):
    """
    Given a job name, collects all assets associated with that job and returns
    them as an array.
    """
    # Collect uploaded assets
    assets = []
    start = os.path.join(PLATFORM_HOME, "jobs", job)
    for root, dirs, files in os.walk(start):
        assets.extend([f for f in files if f.endswith(".jpg") or f.endswith(".png")])
    return assets


def generate_csv(job, *args, **kwargs):
    """
    Given a job name, generates a CSV representing that job and places it in
    the job folder.
    """
    # Collect assets and generate a CSV
    with open(os.path.join(PLATFORM_HOME, "jobs", job, "{}.csv".format(job)), "wb") as fp:
        writer = csv.writer(fp)
        for asset in collect_assets(job):
            writer.writerow([asset])


def register_job(job, *args, **kwargs):
    """
    Registers a new job in the platform (generates CSV and updates index).
    """
    # Generate CSV
    generate_csv(job)

    # Update index
    with open(os.path.join(PLATFORM_HOME, "jobs","index.txt"), "wb") as fp:
        fp.writelines([job])


if __name__ == "__main__":
    register_job(*sys.argv[1:])
