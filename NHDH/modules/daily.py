import numpy as np
import pandas as pd
import zipfile
import os
from NHDH import app

class Daily():
    def __init__(self):
        pass


    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


    def dataframe_to_json(df):
        d = [
            dict([
                (colname, row[i])
                for i, colname in enumerate(df.columns)
            ])
            for row in df.values
        ]
        return d

    def month_by_day_by_tag(self, filename, tag_key, value, fill=None):
        """Report on custom tag key/value pair. Optional fill null values in the
        tag_key column with a default entry e.g. "general"
        Returns two dictionaries containing cumulative cost and detailed cost"""
        cumulative = False
        detailed = False
        file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df = pd.read_csv(file, index_col='UsageStartDate', parse_dates=True, header=0)
        if fill is not None:
                df = df.fillna({tag_key:'%s' %(fill)})
        df = df[np.isfinite(df['SubscriptionId'])]
        gb = df.groupby(by='user:%s' % tag_key)
        gb = gb.get_group(value)

        cost_types = ['Cost', 'UnBlendedCost']

        for cost in cost_types:
            try:
                db = gb.groupby(['ItemDescription']).sum().sort(cost, ascending=False)
                jbb = db[[cost]]
                jbb['Cumulative'] = jbb[cost].cumsum()
                detailed = {value: jbb}

                pb = gb.groupby([lambda x: x.day]).sum()
                jb = pb[[cost]]
                jb['Change'] = jb[cost].pct_change()
                jb['Cumulative'] = jb[cost].cumsum()
                cumulative = {value: jb}

                db = gb.groupby(['ItemDescription']).sum().sort(cost, ascending=False)
                jbb = db[[cost]]
                jbb['Cumulative'] = jbb[cost].cumsum()
                detailed = {value: jbb}
                break
            except:
                continue

        return cumulative, detailed


    def month_by_day(self,filename):
        jb = False
        file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df = pd.read_csv(file, index_col='UsageStartDate', parse_dates=True, header=0)
        df = df[np.isfinite(df['SubscriptionId'])]
        gb = df.groupby([lambda x: x.day]).sum()

        cost_types = ['Cost', 'UnBlendedCost']
        for cost in cost_types:
            jb = self.build_jb(gb, cost)
            if jb:
                break
        return jb


    def build_jb(self, gb, cost):
        try:
            jb = gb[[cost]]
            jb['Change'] = jb[cost].pct_change()
            jb['Cumulative'] = jb[cost].cumsum()
        except:
            jb = False
        return jb


    def month_by_itemdescription(self,filename):
        jb = False
        try:
            #this is for the reports that have blended and unblended costs
            file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            df = pd.read_csv(file, index_col='UsageStartDate', dtype={'ItemDescription': str}, parse_dates=True, header=0)
            df = df[np.isfinite(df['SubscriptionId'])]
            gb = df.groupby(['ItemDescription']).sum().sort('UnBlendedCost', ascending=False)
            jb = gb[['UnBlendedCost']]
            jb['Cumulative'] = jb['UnBlendedCost'].cumsum()
        except:
            #a BIG assumption here but if we don't have unblended cost we must have Cost
            file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            df = pd.read_csv(file, index_col='UsageStartDate', dtype={'ItemDescription': str}, parse_dates=True, header=0)
            df = df[np.isfinite(df['SubscriptionId'])]
            gb = df.groupby(['ItemDescription']).sum().sort('Cost', ascending=False)
            jb = gb[['Cost']]
            jb['Cumulative'] = jb['Cost'].cumsum()
        return jb


    def month_by_az(self,filename):
        jb = False
        try:
            file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            df = pd.read_csv(file, index_col='UsageStartDate', dtype={'AvailabilityZone': str}, parse_dates=True, header=0)
            gb = df.groupby(['ReservedInstance']).sum()
            jb = gb[['UnBlendedCost']]
        except:
            pass
        return jb


    def day_by_itemdescription(t3, filename):
        jb = False
        try:
            file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            df = pd.read_csv(file, index_col='UsageStartDate', parse_dates=True, header=0)
            df_f = df[df['ItemDescription'] == t3]
            gb = df_f.groupby([lambda x: x.day]).sum()
            jb = gb[['UnBlendedCost']]
        except:
            pass
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

