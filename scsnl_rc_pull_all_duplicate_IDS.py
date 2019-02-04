#!/usr/bin/env python


# import subprocess
# subprocess.call(['pip', 'install', 'pycurl'])


import pandas as pd
import os

prefix = '/Users/daelsaid/scratch/scsnl_rc_duplicate_records/'  # parent directory

# rc export of all subj with phone or email not empty
csv = pd.read_csv(os.path.join(
    prefix, 'pii_data_base_all_records.csv'), dtype=str)

new_df = pd.DataFrame()  # set new df
new_df = csv[['record_id', 'pid', 'participant_firstname', 'participant_lastname',
              'participant_dob', 'address_email']]  # set cols for new df

# set new col with cell value reflecting  email duplicated = true/false
new_df["email_duplicated"] = new_df['address_email'].duplicated()

# concat of subj first, last, and dob
new_df['first_last_concat'] = csv['participant_firstname'] + ' ' + \
    csv['participant_lastname'] + ' ' + csv['participant_dob']


new_df['child_info_dup'] = new_df['first_last_concat'].duplicated()

# nans at the end, sort by email and child info
# shows if parent signed up 2 seperate children
new_df.sort_values(by=['address_email', 'child_info_dup'],
                   na_position='last', inplace=True)

for idx, duplications in new_df.groupby(['record_id']):
    if (duplications['child_info_dup'].duplicated()).any() and duplications['email_duplicated'].duplicated().any():
        print idx
        print duplications['address_email'].head()
        print duplications['first_last_concat'].head()


#write to csv
# new_df.to_csv(os.path.join(prefix,'duplicates.csv'))

# TO DO: compare email and child info and if email add true = print child info to see if seperate kids
# TO DO: if email and child info dup = print ID

# TO DO: make into script that exports data, saves csv, then assesses, once check is done
# TO DO: # change rc field to duplicated = 1, and if seperate siblings, change rc sep siblings field = 1

# will be script that pulls data and writes to CSV

# import pycurl, cStringIO
# buf = cStringIO.StringIO()
# data = {
#     'token': '',
#     'content': 'report',
#     'format': 'csv',
#     'report_id': '48927',
#     'rawOrLabel': 'raw',
#     'rawOrLabelHeaders': 'raw',
#     'exportCheckboxLabel': 'false',
#     'returnFormat': 'csv'
# }
# ch = pycurl.Curl()
# ch.setopt(ch.URL, 'https://redcap.stanford.edu/api/')
# ch.setopt(ch.HTTPPOST, data.items())
# ch.setopt(ch.WRITEFUNCTION, buf.write)
# ch.perform()
# ch.close()
# print buf.getvalue()
# buf.close()
#
