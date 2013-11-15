import os
import numpy as np
import pandas as pd
from StringIO import StringIO
import dateutil
import pprint
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import flask_sijax


# InvoiceID	PayerAccountId	LinkedAccountId	RecordType	RecordId	ProductName	RateId	SubscriptionId	PricingPlanId	UsageType	Operation	AvailabilityZone	ReservedInstance	ItemDescription	UsageStartDate	UsageEndDate	UsageQuantity	BlendedRate	BlendedCost	UnBlendedRate	UnBlendedCost	ResourceId	user:Name	user:OWNER-T3	user:SERVICE-ENVIRONMENT	user:SERVICE-NAME	user:SUPPORT-T3

#usagestartdate this day
#pricingPlanId Group by day on this
#sum
#usagequantity
#blendedcost
#unblendedcost
app = Flask(__name__)

# The path where you want the extension to create the needed javascript files
# DON'T put any of your files in this directory, because they'll be deleted!
app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

# You need to point Sijax to the json2.js library if you want to support
# browsers that don't support JSON natively (like IE <= 7)
app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'

flask_sijax.Sijax(app)

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

def month_by_owner():
    file  ='c:/repos/NHDH/csv/371416632205-aws-billing-detailed-line-items-with-resources-and-tags-2013-10.csv'
    df = pd.read_csv(file, index_col='UsageStartDate', parse_dates=True, header=0)
    df = df[np.isfinite(df['SubscriptionId'])]
    gb = df.groupby('user:OWNER-T3').sum().sort('BlendedCost')
    #gbowner = df.mask(lambda x: x['user:OWNER-T3'] == '532500')
    #df_f = df[df['user:OWNER-T3'] == '532500']
    #gb = df.groupby([lambda x: x.day]).sum()
    #gbowner = df.mask(lambda x: x['user:OWNER-T3'] == '532500')
    jb = gb[['BlendedCost']]
    #jb = dataframe_to_json(jb)
    return jb

def day_by_owner_only(t3):
    file  ='c:/repos/NHDH/csv/371416632205-aws-billing-detailed-line-items-with-resources-and-tags-2013-10.csv'
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




@app.route('/')
def index():
    mdf = month_by_owner()
    return render_template('breakdown.html', mdf=mdf)

@flask_sijax.route(app, '/hello')
def hello():
    # Every Sijax handler function (like this one) receives at least
    # one parameter automatically, much like Python passes `self`
    # to object methods.
    # The `obj_response` parameter is the function's way of talking
    # back to the browser
    def t3(obj_response, t3):
        days = day_by_owner_only(t3)
        obj_response.alert('Days are %s' % (days))
        #obj_response.html_append('#'+t3, '<li>%s</li>' % (days))

    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_callback('t3', t3)
        return g.sijax.process_request()

    # Regular (non-Sijax request) - render the page template
    mdf = month_by_owner()
    return render_template('breakdown.html', mdf=mdf)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
