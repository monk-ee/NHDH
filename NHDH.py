import csv
import numpy as np
import pandas as pd
from StringIO import StringIO
import dateutil
import pprint
from flask import Flask


# InvoiceID	PayerAccountId	LinkedAccountId	RecordType	RecordId	ProductName	RateId	SubscriptionId	PricingPlanId	UsageType	Operation	AvailabilityZone	ReservedInstance	ItemDescription	UsageStartDate	UsageEndDate	UsageQuantity	BlendedRate	BlendedCost	UnBlendedRate	UnBlendedCost	ResourceId	user:Name	user:OWNER-T3	user:SERVICE-ENVIRONMENT	user:SERVICE-NAME	user:SUPPORT-T3

#usagestartdate this day
#pricingPlanId Group by day on this
#sum
#usagequantity
#blendedcost
#unblendedcost
app = Flask(__name__)


@app.route('/')
def read_csv():
    file  ='c:/repos/NHDH/csv/371416632205-aws-billing-detailed-line-items-with-resources-and-tags-2013-10.csv'
    df = pd.read_csv(file, index_col='UsageStartDate', parse_dates=True, header=0)
    df = df[np.isfinite(df['SubscriptionId'])]
    print df
    #gb = df.groupby('user:OWNER-T3').sum().sort('BlendedCost')
    #gbowner = df.mask(lambda x: x['user:OWNER-T3'] == '532500')
    gb = df.groupby([lambda x: x.day]).sum()
    #gbowner = df.mask(lambda x: x['user:OWNER-T3'] == '532500')
    jb = gb[['BlendedCost']]
    print jb
    return "hello"

if __name__ == '__main__':
    app.run(debug=True)
