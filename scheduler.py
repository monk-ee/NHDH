#!/usr/bin/env python
__author__ = 'monk-ee'

"""This module schedules the picking up of the bucket file.
"""
from NHDH.modules.fetch import *
from NHDH import app
import logging
from apscheduler.scheduler import Scheduler


class scheduler():

    def __init__(self):
        logging.basicConfig(filename=str(app.config['CONFIG']['logfile']),level=logging.INFO)
        sched = Scheduler(daemon=True)
        sched.start()
        sched.add_interval_job(lambda: self.fetch_report_by_interval(), hours=str(app.config['CONFIG']['scheduler']['hourly_interval']))
        while True:
            pass

    def fetch_report_by_interval(self):
        ff = Fetch()
        ff.fetch(scheduler=True)

my_sched = scheduler()