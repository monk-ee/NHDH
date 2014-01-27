#!/usr/bin/env python
__author__ = 'monkee'
__version__ = '1.0.1'

# @todo df.groupby(['SubscribtionId', 'BlendedCost'])
# @todo select key/header to group on
# @todo go back in time for a fetch as a dropdown
# @todo detailed csv/pdf as an attachment
# @todo filenames as keys
# @todo add config.yml as actual app configuration items


import os
import locale
import yaml
from flask import Flask
from werkzeug import secure_filename
from NHDH.modules.cache import cache as cache


#immutable configuration items
locale.setlocale(locale.LC_ALL, '')

#app configuration items
app = Flask(__name__)
app.secret_key = 'sdakjkdsjksjkjaskjdkaskjdkjkjdkjkjkjdksjkajlkjaskljdkljklsdj'
app.config['UPLOAD_FOLDER'] = os.path.abspath('NHDH/csv')
app.config['CONFIG_FILE'] = os.path.abspath('NHDH/conf/config.yml')
app.config['ALLOWED_EXTENSIONS'] = set(['zip'])
app.config['CSV_FOLDER'] = os.path.abspath('NHDH/csv/')

#import yaml here
configStr = open(app.config['CONFIG_FILE'], 'r')
app.config['CONFIG'] = yaml.load(configStr)
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

#import views here
from NHDH.views.main import main as main
app.register_blueprint(main)
