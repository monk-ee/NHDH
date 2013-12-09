__author__ = 'monkee'
__version__ = '1.0.1'

# @todo df.groupby(['SubscribtionId', 'BlendedCost'])
# @todo select key/header to group on
# @todo go back in time for a fetch as a dropdown
# @todo detailed csv/pdf as an attachment
# @todo filenames as keys

import os
import locale

from flask import Flask
from werkzeug import secure_filename


#static configuration items
UPLOAD_FOLDER = os.path.abspath('NHDH/csv')
ALLOWED_EXTENSIONS = set(['zip'])
locale.setlocale(locale.LC_ALL, '')

#app configuration items
app = Flask(__name__)
app.secret_key = 'sdakjkdsjksjkjaskjdkaskjdkjkjdkjkjkjdksjkajlkjaskljdkljklsdj'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# The path where you want the extension to create the needed javascript files
# DON'T put any of your files in this directory, because they'll be deleted!
app.config["SIJAX_STATIC_PATH"] = os.path.join('../', os.path.dirname(__file__), 'static/js/sijax/')

# You need to point Sijax to the json2.js library if you want to support
# browsers that don't support JSON natively (like IE <= 7)
app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'



#import views here
import NHDH.views
import NHDH.ajaxviews









#if __name__ == '__main__':
#    app.run(host='0.0.0.0',debug=True)
