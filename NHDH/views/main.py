from NHDH.modules.daily import *
from NHDH.modules.fetch import *
from NHDH.modules.py_email import *
from NHDH.modules.cache import cache
from datetime import datetime
from dateutil import parser
from StringIO import *
from flask import Blueprint, request, redirect, url_for,  \
     render_template, flash, send_from_directory, send_file
from werkzeug import secure_filename

main  = Blueprint('main', __name__)
cache_timeout = int(app.config['CONFIG']['cache']['timeout'])

@main.route('/')
def list_reports():
    os.chdir(app.config['UPLOAD_FOLDER'])
    csv = list()
    for files in os.listdir("."):
        if files.endswith(".csv"):
            csv.append(files)
    return render_template('files.html', csv=csv)

@main.route('/dailyreport/<filename>')
@cache.cached(timeout=cache_timeout)
def daily(filename):
    daily = Daily()
    mdf = daily.month_by_day(filename)
    return render_template('dailyreport.html',
                           mdf=mdf)

@main.route('/dailygraph/<filename>')
@cache.cached(timeout=cache_timeout)
def dailygraph(filename):
    daily = Daily()
    mdf = daily.month_by_day(filename)
    return render_template('dailygraph.html',
                           mdf=mdf)

@main.route('/itemreport/<filename>')
@cache.cached(timeout=cache_timeout)
def item(filename):
    daily = Daily()
    idf = daily.month_by_itemdescription(filename)
    return render_template('itemreport.html',
                           idf=idf)

@main.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Successful file upload.')
            return redirect(url_for('unzip_file',
                                    filename=filename))
        else:
            flash('Invalid file type or file error.')
    return render_template('upload.html')

@main.route('/uploads/<filename>')
def unzip_file(filename):
    unzip(os.path.join(app.config['UPLOAD_FOLDER'],filename),app.config['UPLOAD_FOLDER'])
    #return ''
    return redirect(url_for('list_reports',
                                    filename=filename))

@main.route('/fetch')
def fetch_zip():
    ff = Fetch()
    ff.fetch()
    #return ''
    return redirect('/')

@main.route('/csv/<filename>')
@cache.cached(timeout=cache_timeout)
def serve_csv(filename):
    daily = Daily()
    mdf = daily.month_by_day(filename)
    buffer = StringIO()
    mdf.to_csv(buffer,encoding='utf-8')
    buffer.seek(0)
    return send_file(buffer,
                     attachment_filename="test.csv",
                     mimetype='text/csv')

@main.route('/mail/<filename>')
def serve_mail(filename):
    daily = Daily()
    mdf = daily.month_by_day(filename)
    html = render_template('dailymail.html',
                           mdf=mdf)
    dt = datetime.now()
    show = dt.strftime("%A %d %B %Y")
    try:
        py_email('Daily Report '+ show, html)
        flash('Successfully sent daily mail.')
        return redirect('/')
    except smtplib.SMTPException, emsg:
        #return ' SMTPException : '+str(emsg)
        flash(' SMTPException : '+str(emsg))
        return redirect('/')


@main.route('/itemmail/<filename>')
def item_mail(filename):
    daily = Daily()
    idf = daily.month_by_itemdescription(filename)
    html = render_template('itemmail.html',
                           idf=idf)
    dt = datetime.now()
    show = dt.strftime("%A %d %B %Y")
    try:
        py_email('Item Breakdown Report '+ show, html)
        flash('Successfully sent item breakdown mail.')
        return redirect('/')
    except smtplib.SMTPException, emsg:
        #return ' SMTPException : '+str(emsg)
        flash(' SMTPException : '+str(emsg))
        return redirect('/')

@main.route('/itemcsv/<filename>')
@cache.cached(timeout=cache_timeout)
def serve_itemcsv(filename):
    mdf = month_by_owner_item(filename)
    buffer = StringIO()
    mdf.to_csv(buffer,encoding='utf-8')
    buffer.seek(0)
    return send_file(buffer,
                     attachment_filename="test.csv",
                     mimetype='text/csv')

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')