
from daily import *
from fetch import *
from datetime import datetime
from StringIO import *
from flask import request, redirect, url_for,  \
     render_template, flash, send_from_directory,  send_file
from py_email import *

@app.route('/')
def list_reports():
    os.chdir(app.config['UPLOAD_FOLDER'])
    csv = list()
    for files in os.listdir("."):
        if files.endswith(".csv"):
            csv.append(files)
    return render_template('files.html', csv=csv)

@app.route('/dailyreport/<filename>')
def daily(filename):
    daily = Daily()
    mdf = daily.month_by_day(filename)
    return render_template('dailyreport.html',
                           mdf=mdf)

@app.route('/upload', methods=['GET', 'POST'])
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

@app.route('/uploads/<filename>')
def unzip_file(filename):
    unzip(os.path.join(app.config['UPLOAD_FOLDER'],filename),app.config['UPLOAD_FOLDER'])
    #return ''
    return redirect(url_for('list_reports',
                                    filename=filename))

@app.route('/fetch')
def fetch_zip():
    ff = Fetch()
    ff.fetch()
    #return ''
    return redirect('/')

@app.route('/csv/<filename>')
def serve_csv(filename):
    daily = Daily()
    mdf = daily.month_by_day(filename)
    buffer = StringIO()
    mdf.to_csv(buffer,encoding='utf-8')
    buffer.seek(0)
    return send_file(buffer,
                     attachment_filename="test.csv",
                     mimetype='text/csv')

@app.route('/mail/<filename>')
def serve_mail(filename):
    daily = Daily()
    mdf = daily.month_by_day(filename)
    html = render_template('dailymail.html',
                           mdf=mdf)
    dt = datetime.now()
    show = dt.strftime("%A %d %B %Y")
    try:
        py_email('Daily Report '+ show, html)
        return redirect('/')
    except smtplib.SMTPException, emsg:
        return ' SMTPException : '+str(emsg)

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