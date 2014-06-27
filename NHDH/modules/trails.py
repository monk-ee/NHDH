__author__ = 'monk-ee'

"""This module provides an interface to the billing report
in the amazon S3 billing bucket.
"""

import os
import boto.cloudtrail

from datetime import datetime
from flask import flash
from NHDH import app


class Trails():
    conn = ""
    region = 'ap-southeast-2'


    def __init__(self):
        self.cloudtrail_connect_to_region()


    def cloudtrail_connect_to_region(self):
        try:
            self.conn = boto.cloudtrail.connect_to_region(self.region)
        except:
            #done again
            exit("Failed to connect to Cloudtrail API")


    def show_trails(self):
        trails = self.conn.describe_trails()
        print(trails)