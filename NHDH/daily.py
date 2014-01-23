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
        try:
            file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            df = pd.read_csv(file, index_col='UsageStartDate', parse_dates=True, header=0)
            if fill is not None:
                df = df.fillna({tag_key:'%s' %(fill)})
            df = df[np.isfinite(df['SubscriptionId'])]
            gb = df.groupby(by='user:%s' % tag_key)
            gb = gb.get_group(value)
            
            # work out product detailed breakdown for current month so far
            db = gb.groupby(['ItemDescription']).sum().sort('UnBlendedCost', ascending=False)
            jbb = db[['UnBlendedCost']]
            jbb['Cumulative'] = jbb['UnBlendedCost'].cumsum()
            detailed = {value: jbb}

            # work out cumulative product cost for current month so far
            pb = gb.groupby([lambda x: x.day]).sum()
            jb = pb[['UnBlendedCost']]
            jb['Change'] = jb['UnBlendedCost'].pct_change()
            jb['Cumulative'] = jb['UnBlendedCost'].cumsum()
            cumulative = {value: jb}
        except:
            pass
        return cumulative, detailed


    def month_by_day(self,filename):
        file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df = pd.read_csv(file, index_col='UsageStartDate', parse_dates=True, header=0)
        df = df[np.isfinite(df['SubscriptionId'])]
        gb = df.groupby([lambda x: x.day]).sum()
        jb = gb[['Cost']]
        jb['Change'] = jb['Cost'].pct_change()
        jb['Cumulative'] = jb['Cost'].cumsum()
        return jb

    def month_by_itemdescription(self,filename):
        file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df = pd.read_csv(file, index_col='UsageStartDate', dtype={'ItemDescription': str}, parse_dates=True, header=0)
        df = df[np.isfinite(df['SubscriptionId'])]
        gb = df.groupby(['ItemDescription']).sum().sort('Cost', ascending=False)
        jb = gb[['Cost']]
        jb['Cumulative'] = jb['Cost'].cumsum()
        return jb


    def month_by_az(self,filename):
        file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df = pd.read_csv(file, index_col='UsageStartDate', dtype={'AvailabilityZone': str}, parse_dates=True, header=0)
        gb = df.groupby(['ReservedInstance']).sum()
        jb = gb[['Cost']]
        return jb


    def day_by_itemdescription(t3, filename):
        file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df = pd.read_csv(file, index_col='UsageStartDate', parse_dates=True, header=0)
        df_f = df[df['ItemDescription'] == t3]
        gb = df_f.groupby([lambda x: x.day]).sum()
        jb = gb[['Cost']]
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

