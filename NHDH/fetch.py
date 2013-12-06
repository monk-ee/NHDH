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

class Fetch():
    configFile = os.path.abspath('NHDH/config.yml')
    csvFolder = os.path.abspath('NHDH/csv')

    def __init__(self):
        #load configuration
        self.configStr = open(self.configFile, 'r')
        self.configObj =  yaml.load(self.configStr)
        #now set detailed billing file
        self.billingFile = str(self.configObj['s3']['account_number'])+"-aws-billing-detailed-line-items-with-resources-and-tags-"+self.datefilename()+".csv.zip"
        self.billingZip = os.path.abspath('NHDH/csv/'+self.billingFile)

    def datefilename(self):
        dt = datetime.now()
        return dt.strftime("%Y-%m")

    def fetch(self):
        # get a bucket connection
        bucketConn = S3Connection(self.configObj['s3']['aws_access_key'], self.configObj['s3']['aws_secret_key'])
        #file name
        billingHandle = bucketConn.get_bucket(self.configObj['s3']['billing_bucket'])
        #key object fudging
        billingFileNameKey = Key(billingHandle)
        billingFileNameKey.key = self.billingFile
        #fetch the file to a temporary place on the filesystem
        try:
                retrieveFile = billingFileNameKey.get_contents_to_filename(self.billingZip)
        except boto.exception.S3ResponseError, emsg:
                print(' S3ResponseError : '+self.billingFile+' '+str(emsg[0])+' '+emsg[1]+' '+str(emsg[2])+'\n')

    def unzipper(self):
        zipHandle = zipfile.ZipFile(self.billingZip, mode='r')
        for subfile in zipHandle.namelist():
            zipHandle.extract(subfile, self.csvFolder)