#!/usr/bin/env python
# to run this script you need to have pycurl downloaded (https://github.com/pycurl/pycurl)
# add path and your redcap token
# run in terminal window: python beam_clinical_assessment_scores_to_csv.py

import pycurl
import cStringIO
import string
import collections
import time
import csv
from itertools import groupby
import pandas

# SET PATH VARIABLE FOR CSV OUTPUT HERE #example: '/Volumes/Smurf-Village/home/daelsaid/redcap_report.csv'
redcap_report_output = ''

# pulling data from clinical assessment scores - a redcap survey based on all the different clinical survey arms in the project
buf = cStringIO.StringIO()
data = {E1F83E6A50C2F520800A49294B84C1B2',
    'content': 'report',
    'format': 'csv',
    'report_id': '22120',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'returnFormat': 'csv'
}

ch = pycurl.Curl()
ch.setopt(ch.URL, 'https://redcap.stanford.edu/api/')
ch.setopt(ch.HTTPPOST, data.items())
ch.setopt(ch.WRITEFUNCTION, buf.write)
ch.perform()
ch.close()
patient_clinical_scores = buf.getvalue()  # set variable to report output
buf.close()

# Prep the output to be parsed
subj_clinical_report_prep1 = str(object=patient_clinical_scores)
subj_clinical_report_prep1 = subj_clinical_report_prep1.replace(' ', '_')
subj_clinical_report_prep1 = subj_clinical_report_prep1.replace('"', '')
subj_clinical_report_prep2 = [subj_clinical_report_prep1]

# splitting lines to be split by commas so we can index
subj_clinical_report_corrected = []
for subj_lines in subj_clinical_report_prep2:
    lines = subj_lines.split()
    for idx, val in enumerate(lines):
        subj_clinical_report_corrected.append(val.split(','))

# create a dataframe to hold parsed and split output
clinical_assessment_scores_df = pandas.DataFrame(
    data=subj_clinical_report_corrected)
length_of_data_frame = len(clinical_assessment_scores_df)


print clinical_assessment_scores_df
with open(redcap_report_output, 'wb') as csvfile:
    clinical_assessment_scores_df[0:length_of_data_frame].to_csv(
        redcap_report_output, index=False, header=False)
# header=false and index=false prevents the row and column indexes to be present
