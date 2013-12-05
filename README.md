# NHDH

Boiler for AWS CSV

## Quickstart

### Debian/Ubuntu

(Only debian/ubuntu instructions for now until I test it all out on RHEL)

Ensure you can build the required python libs by installing python development libraries:

`sudo apt-get install python-dev`

Install the required python libraries:

`sudo pip install -r requirements`

Run it up:

`python NHDH.py`

Test by going to:
<http://localhost:5000/> or <http://yourservername:5000/>

### RHEL

TODO...

### Windows

* You'll need Microsoft Visual Studio (true?) to install the pandas and numpy python libraries.
* pip for windows is probably easiest? <https://sites.google.com/site/pydatalog/python/pip-for-windows>