__author__ = 'monk-ee'

"""This module provides an interface to the billing report
in the amazon S3 billing bucket.
"""

import os
import boto
import zipfile
from boto.s3.connection import S3Connection
from datetime import datetime
from boto.s3.key import Key
from flask import flash
from NHDH import app


class Fetch():


    def __init__(self):
        #now set detailed billing file
        self.billingCsv = str(app.config['CONFIG']['s3']['account_number'])+"-aws-billing-detailed-line-items-with-resources-and-tags-"+self.datefilename()+".csv"
        self.billingFile = str(app.config['CONFIG']['s3']['account_number'])+"-aws-billing-detailed-line-items-with-resources-and-tags-"+self.datefilename()+".csv.zip"
        self.billingZip = os.path.abspath(app.config['CSV_FOLDER']+self.billingFile)

    def datefilename(self):
        dt = datetime.now()
        return dt.strftime("%Y-%m")

    def fetch(self,scheduler=False):
        # get a bucket connection
        bucketConn = S3Connection(app.config['CONFIG']['s3']['aws_access_key'], app.config['CONFIG']['s3']['aws_secret_key'])
        #file name
        billingHandle = bucketConn.get_bucket(app.config['CONFIG']['s3']['billing_bucket'])
        #key object fudging
        billingFileNameKey = Key(billingHandle)
        billingFileNameKey.key = self.billingFile
        #fetch the file to a temporary place on the filesystem
        try:
                retrieveFile = billingFileNameKey.get_contents_to_filename(self.billingZip)
                if scheduler:
                    print "Successfully got file from S3."
                else:
                    flash('Successfully got file from S3.')
                self.unzipper()
                self.unlink()
        except boto.exception.S3ResponseError, emsg:
                if scheduler:
                    print ' S3ResponseError : '+self.billingFile+' '+str(emsg[0])+' '+emsg[1]+' '+str(emsg[2])
                else:
                    flash(' S3ResponseError : '+self.billingFile+' '+str(emsg[0])+' '+emsg[1]+' '+str(emsg[2]))


    def unzipper(self):
        zipHandle = zipfile.ZipFile(self.billingZip, mode='r')
        for subfile in zipHandle.namelist():
            zipHandle.extract(subfile, app.config['CSV_FOLDER'])

    def unlink(self):
        try:
            with open(self.billingZip):
             os.remove(self.billingZip)
        except IOError:
             flash('Could not delete downloaded zip file.')
