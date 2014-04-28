#!/usr/bin/env python
__author__ = 'monkee'
__version__ = '1.1.0'

# @todo df.groupby(['SubscribtionId', 'BlendedCost'])
# @todo select key/header to group on
# @todo go back in time for a fetch as a dropdown
# @todo detailed csv/pdf as an attachment
# @todo filenames as keys
# @todo add config.yml as actual app configuration items


import os
import locale
import yaml
from flask import Flask, render_template,request, redirect, url_for

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

#Identity
from flask.ext.principal import Principal, PermissionDenied
principals = Principal(app, skip_static=True)

#flask-login
from flask.ext.login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g
from flask.ext.login import login_user , logout_user , current_user , login_required

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form['email']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(email=email,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user, remember = remember_me)
    flash('Logged in successfully')
    return redirect('/')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.before_request
def before_request():
    g.user = current_user

@app.errorhandler(PermissionDenied)
def handle_permission_error(error):
    #TODO Log permission error
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

#import yaml here
configStr = open(app.config['CONFIG_FILE'], 'r')
app.config['CONFIG'] = yaml.load(configStr)

#cache init here
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

from NHDH.models import User

#import views here
from NHDH.views.main import main as main
app.register_blueprint(main)
