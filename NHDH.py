import os
import locale
import numpy as np
import pandas as pd
import zipfile
from StringIO import StringIO
import dateutil
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_from_directory, Response, send_file
from werkzeug import secure_filename
import flask_sijax

# Set the folder to store uploaded csv files
UPLOAD_FOLDER = os.path.abspath('csv')

# allowed extensions of uploaded files
ALLOWED_EXTENSIONS = set(['zip'])

locale.setlocale(locale.LC_ALL, '')

# @todo csv output file
# @todo df.groupby(['SubscribtionId', 'BlendedCost'])
# @todo sum only cost columns
# @todo select key/header to group on
# @todo do locale for money correctly
# @todo direct fetching of csvs from specified s3 bucket(s) with bucket permissions (role/simple auth?)



# InvoiceID	PayerAccountId	LinkedAccountId	RecordType	RecordId	ProductName	RateId	SubscriptionId	PricingPlanId	UsageType	Operation	AvailabilityZone	ReservedInstance	ItemDescription	UsageStartDate	UsageEndDate	UsageQuantity	BlendedRate	BlendedCost	UnBlendedRate	UnBlendedCost	ResourceId	user:Name	user:OWNER-T3	user:SERVICE-ENVIRONMENT	user:SERVICE-NAME	user:SUPPORT-T3
# plotly key dvswdkf6sp
#py = plotly.plotly(username='monk-ee', key='dvswdkf6sp')
#usagestartdate this day
#pricingPlanId Group by day on this
#sum
#usagequantity
#blendedcost
#unblendedcost
app = Flask(__name__)
app.secret_key = 'sdakjkdsjksjkjaskjdkaskjdkjkjdkjkjkjdksjkajlkjaskljdkljklsdj'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# The path where you want the extension to create the needed javascript files
# DON'T put any of your files in this directory, because they'll be deleted!
app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

# You need to point Sijax to the json2.js library if you want to support
# browsers that don't support JSON natively (like IE <= 7)
app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'

flask_sijax.Sijax(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def dataframe_to_json(df):
    print df.values
    print df.index
    d = [
        dict([
            (colname, row[i])
            for i,colname in enumerate(df.columns)
        ])
        for row in df.values
        ]
    print d
    return d

def month_by_owner(filename):
    #file  ='c:/repos/NHDH/csv/371416632205-aws-billing-detailed-line-items-with-resources-and-tags-2013-10.csv'
    file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(file, index_col='UsageStartDate', dtype={'user:OWNER-T3' : str}, parse_dates=True, header=0)
    df = df[np.isfinite(df['SubscriptionId'])]
    df['user:OWNER-T3'] = df['user:OWNER-T3'].fillna('Untagged')
    df['user:OWNER-T3'] = df['user:OWNER-T3'].astype(str)
    #gb = df.groupby('user:OWNER-T3').sum().sort('BlendedCost')
    gb = df.groupby(['user:OWNER-T3']).sum()
    #gbowner = df.mask(lambda x: x['user:OWNER-T3'] == '532500')
    #df_f = df[df['user:OWNER-T3'] == '532500']
    #gb = df.groupby([lambda x: x.day]).sum()
    #gbowner = df.mask(lambda x: x['user:OWNER-T3'] == '532500')
    print gb
    jb = gb[['BlendedCost']]
    pd.options.display.float_format = '{:20,.2f}'.format
    #jb = dataframe_to_json(jb)
    print jb
    return jb

def month_by_owner_item(filename):
    #file  ='c:/repos/NHDH/csv/371416632205-aws-billing-detailed-line-items-with-resources-and-tags-2013-10.csv'
    file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(file, index_col='UsageStartDate', dtype={'user:OWNER-T3' : str}, parse_dates=True, header=0)
    df = df[np.isfinite(df['SubscriptionId'])]
    df['user:OWNER-T3'] = df['user:OWNER-T3'].fillna('Untagged')
    df['user:OWNER-T3'] = df['user:OWNER-T3'].astype(str)
    #gb = df.groupby('user:OWNER-T3').sum().sort('BlendedCost')
    gb = df.groupby(['ItemDescription','user:OWNER-T3']).sum()
    #gbowner = df.mask(lambda x: x['user:OWNER-T3'] == '532500')
    #df_f = df[df['user:OWNER-T3'] == '532500']
    #gb = df.groupby([lambda x: x.day]).sum()
    #gbowner = df.mask(lambda x: x['user:OWNER-T3'] == '532500')
    print gb
    jb = gb[['BlendedCost']]
    #jb = dataframe_to_json(jb)
    print jb
    return jb

def day_by_owner_only(t3,filename):
    #file  ='c:/repos/NHDH/csv/371416632205-aws-billing-detailed-line-items-with-resources-and-tags-2013-10.csv'
    file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(file, index_col='UsageStartDate', parse_dates=True, header=0)
    df = df[np.isfinite(df['SubscriptionId'])]
    #gb = df.groupby('user:OWNER-T3').sum().sort('BlendedCost')
    #gbowner = df.mask(lambda x: x['user:OWNER-T3'] == '532500')
    df_f = df[df['user:OWNER-T3'] == t3]
    gb = df_f.groupby([lambda x: x.day]).sum()
    #gbowner = df.mask(lambda x: x['user:OWNER-T3'] == '532500')
    jb = gb[['BlendedCost']]
    print jb
    return jb

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)

def index():
    mdf = month_by_owner()
    return render_template('breakdown.html', mdf=mdf)


@app.route('/')
def list_reports():
    os.chdir(app.config['UPLOAD_FOLDER'])
    csv = list()
    for files in os.listdir("."):
        if files.endswith(".csv"):
            csv.append(files)
    return render_template('files.html', csv=csv)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('unzip_file',
                                    filename=filename))
        else:
            flash('Invalid file type or file error.')
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def unzip_file(filename):
    unzip(os.path.join(app.config['UPLOAD_FOLDER'],filename),app.config['UPLOAD_FOLDER'])
    #return ''
    return redirect(url_for('list_reports',
                                    filename=filename))

@app.route('/csv/<filename>')
def serve_csv(filename):
    mdf = month_by_owner(filename)
    buffer = StringIO()
    mdf.to_csv(buffer,encoding='utf-8')
    buffer.seek(0)
    return send_file(buffer,
                     attachment_filename="test.csv",
                     mimetype='text/csv')

@app.route('/itemcsv/<filename>')
def serve_itemcsv(filename):
    mdf = month_by_owner_item(filename)
    buffer = StringIO()
    mdf.to_csv(buffer,encoding='utf-8')
    buffer.seek(0)
    return send_file(buffer,
                     attachment_filename="test.csv",
                     mimetype='text/csv')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@flask_sijax.route(app, '/report/<filename>')
def owner(filename):
    # Every Sijax handler function (like this one) receives at least
    # one parameter automatically, much like Python passes `self`
    # to object methods.
    # The `obj_response` parameter is the function's way of talking
    # back to the browser
    def t3(obj_response, t3):
        days = day_by_owner_only(t3, filename)
        obj_response.alert('Days are %s' % (days))
        #obj_response.html_append('#'+t3, '<li>%s</li>' % (days))

    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_callback('t3', t3)
        return g.sijax.process_request()

    # Regular (non-Sijax request) - render the page template
    mdf = month_by_owner(filename)
    return render_template('breakdown.html',
                           mdf=mdf,
                           filename=filename)

@flask_sijax.route(app, '/itemreport/<filename>')
def item(filename):
    # Every Sijax handler function (like this one) receives at least
    # one parameter automatically, much like Python passes `self`
    # to object methods.
    # The `obj_response` parameter is the function's way of talking
    # back to the browser
    def t3(obj_response, t3):
        days = day_by_owner_only(t3, filename)
        obj_response.alert('Days are %s' % (days))
        #obj_response.html_append('#'+t3, '<li>%s</li>' % (days))

    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_callback('t3', t3)
        return g.sijax.process_request()

    # Regular (non-Sijax request) - render the page template
    mdf = month_by_owner_item(filename)
    return render_template('itembreakdown.html',
                           mdf=mdf,
                           filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
