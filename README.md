# NHDH a Stats Reducer for AWS CSV
The purpose of this program is to reduce the large number of line items in a detailed billing file to a daily/monthly summary.

#### What it does
 - Downloads direct from your billing bucket
 - Displays a monthly summary including daily total, % daily difference, running total
 - Emails the monthly summary to a list of recipients
 - processes uploaded billing zip files
 - provides a summary csv for download

#### What we are currently working on
 - a better ui - to replace the crappy one monk-ee knocked up
 - multiple report formats
 - js graphing
 - administrative panel
 - json gui

## Quickstart
 - You will need to fill out the configuration data in the config.yml.sample and save it as config.yml
 - s3
 - account_number   : '' #your Amazon Account number
 - billing_bucket   : '' #the name of your billing bucket
 - name             : '' #the name of your administrative account user - currently not used
 - aws_access_key   : '' #user access key
 - aws_secret_key   : '' #user secret key
 - smtp
 - name             : '' # name of account user - ses specific - currently not used
 - user             : '' # user account for smtp auth
 - password         : '' # user password for smtp auth
 - server           : '' # smtp server without port
 - sender_address   : 'me@mysite.com' #smtp from address
 - port             : '587' # we always engage tls
 - recipients: # this is an array of accounts
 - address     : 'test@test.com'
 - general:
 - format           : 'standard' # we have noticed that there are different formats for the bills
 - debug            : 'True' # bugginess to be reported
 - filter           : 'not implemented' # this will be a user based filter - currently not used
 - time_zone        : 'Australia/Brisbane' # timezone
 - version          : '1.0.0' # current build version - Don't touch please

 - on the AWS side you will need to ensure that the S3 billing bucket has a policy to allow access to it and that programmatic access to billing is enabled.

 - resolve all dependencies

 - you can change the port in the runserver.py

### Debian/Ubuntu

(Only debian/ubuntu instructions for now until I test it all out on RHEL)

Ensure you can build the required python libs by installing python development libraries:

`sudo apt-get install python-dev`

Install the required python libraries:

`sudo pip install -r requirements`

### NHDH has been changed to a simple package.

Run it up:

`python runserver.py`

Test by going to:
<http://localhost:5000/> or <http://yourservername:5000/>

### RHEL

TODO... TOOHARD

### Windows

* You'll need Microsoft Visual Studio if you want to compile the pandas and numpy python libraries yourself.
* You can download precompiled versions of pandas and numpy from pypi site
* pip for windows is easy too <https://sites.google.com/site/pydatalog/python/pip-for-windows>

### Screenshots
Screenshot of email body:

![ScreenShot](https://raw.github.com/monk-ee/NHDH/master/screenshots/email_shot.png)

### Contributors
@monkee_magic - hidden code development - poor html and css
@geekpetedotcom - hidden code and quality control
@linkthief - the stuff that everyone sees
