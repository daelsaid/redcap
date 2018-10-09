#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May  4 01:14:28 2018

@author: dawlat_local
"""


token = 'BE22B1E1DCECC4631C50A7EFC7911EE2'
url = 'https://redcap.stanford.edu/api/'

#
# curl -X POST -H "Cache-Control: no-cache" -F "token=BE22B1E1DCECC4631C50A7EFC7911EE2" -F "record=" -F "format=json" -F "delta=96:00:00" "https://redcap.stanford.edu/plugins/open/last_modified.php"
#

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 18:04:40 2018

@author: dawlat_local
"""

#!/usr/bin/env python

import pycurl
import cStringIO
import pandas
import time
from prettytable import PrettyTable

current_date = str(time.strftime('%Y/%m/%d'))
current_date.replace('/', '-')

buf = cStringIO.StringIO()
data = {
    'token': 'BE22B1E1DCECC4631C50A7EFC7911EE2',
    'content': 'report',
    'format': 'csv',
    'report_id': '34176',
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
redcap_output = buf.getvalue()
buf.close()

prep_list = str(object=redcap_output)
prepped_list = [prep_list.replace(' ', '_').replace('"', '')]

best_corrected = []
for best_lines in prepped_list:
    lines = best_lines.split()
    for idx, val in enumerate(lines):
        best_corrected.append(val.split(','))


numbers_df = pandas.DataFrame(data=best_corrected)
best_columns = numbers_df[0:1].values.tolist()
numbers_df.columns = best_columns
numbers = numbers_df[1:]

tp1_pt = []
tp1_inprocess = []
tp2_pt = []
tp2_inprocess = []
sixmonth = []
tp1_hc = []
tp2_hc = []
hv_all = []


intake_tp1 = []

for x, y in numbers.groupby('redcap_event_name'):
    if y['enrolled_for'].values[4] == '1':
        tp1_pt.append(y['date_of_tp2'].values.tolist())
        sixmonth.append(y['six_month_followup_date'].values.tolist())
        tp2_pt.append(y['date_of_tp2_appointment_2'].values.tolist())
    if y['enrolled_for'].values[4] == '3':
        tp1_hc.append(y['date_of_tp2'].values.tolist())
        tp2_hc.append(y['date_of_tp2_appointment_2'].values.tolist())
    else:
        hv_all.append(y['date_of_tp2'].values.tolist())

tp1_dates = [(tp1, val) for tp1, val in enumerate(tp1_pt)]


tp1_completed_patients = numbers.groupby('redcap_event_name')[
    'time_point_completion_master'].value_counts()[3]
tp1_completed_hv = numbers.groupby('redcap_event_name')[
    'time_point_completion_master'].value_counts()[7]
tp1_completed_hc = numbers.groupby('redcap_event_name')[
    'time_point_completion_master'].value_counts()[0]

tp2_completed_patients = numbers.groupby('redcap_event_name')[
    'time_point_completion_master1'].value_counts()[4]
tp2_completed_hc = numbers.groupby('redcap_event_name')[
    'time_point_completion_master1'].value_counts()[0]
six_month_followup = numbers.groupby('redcap_event_name')[
    'six_month_followup'].value_counts()[2]

intake_pt_tp1 = numbers.groupby('redcap_event_name')[
    'clinical_assessment_scores_complete'].value_counts()[2]
tms_pt_tp1 = numbers.groupby('redcap_event_name')[
    'tms_eeg_completed'].value_counts()[2]
mri_pt_tp1 = numbers.groupby('redcap_event_name')[
    'mri_completed_1'].value_counts()[2]
saline_pt_tp1 = numbers.groupby('redcap_event_name')[
    'did_the_participant_comple'].value_counts()[4]
dry_pt_tp1 = numbers.groupby('redcap_event_name')[
    'dry_eeg_completion'].value_counts()[4]
webneuro_pt_tp1 = numbers.groupby('redcap_event_name')[
    'webneuro_session_completed'].value_counts()[2]
vm_react_pt_tp1 = numbers.groupby('redcap_event_name')[
    'inquisit_task_completed'].value_counts()[2]

intake_pt_tp2 = numbers.groupby('redcap_event_name')[
    'clinical_assessment_scores_complete'].value_counts()[4]
vm_react_pt_tp2 = numbers.groupby('redcap_event_name')[
    'inquisit_task_completed'].value_counts()[7]
webneuro_pt_tp2 = numbers.groupby('redcap_event_name')[
    'webneuro_session_completed'].value_counts()[8]
tms_pt_tp2 = numbers.groupby('redcap_event_name')[
    'tms_eeg_completed'].value_counts()[9]
mri_pt_tp2 = numbers.groupby('redcap_event_name')[
    'mri_completed_1'].value_counts()[8]
dry_pt_tp2 = numbers.groupby('redcap_event_name')[
    'dry_eeg_completion'].value_counts()[11]
saline_pt_tp2 = numbers.groupby('redcap_event_name')[
    'did_the_participant_comple'].value_counts()[10]

saline_hc_tp1 = numbers.groupby('redcap_event_name')[
    'did_the_participant_comple'].value_counts()[0]

intake_hv = numbers.groupby('redcap_event_name')[
    'clinical_assessment_scores_complete'].value_counts()[7]
webneuro_hv = numbers.groupby('redcap_event_name')[
    'webneuro_session_completed'].value_counts()[5]
vm_react_hv = numbers.groupby('redcap_event_name')[
    'inquisit_task_completed'].value_counts()[4]
tms_hv = numbers.groupby('redcap_event_name')[
    'tms_eeg_completed'].value_counts()[5]
mri_hv = numbers.groupby('redcap_event_name')[
    'mri_completed_1'].value_counts()[5]
saline_hv_tp1 = numbers.groupby('redcap_event_name')[
    'did_the_participant_comple'].value_counts()[6]
dry_hv_tp1 = numbers.groupby('enrolled_for')[
    'dry_eeg_completion'].value_counts()[8]


proc = PrettyTable()

proc.field_names = ['-', 'Intake', 'Dry EEG',
                    'Saline EEG', 'VMREACT', 'Webneuro', 'fMRI', 'TMS/EEG']
proc.add_row(["Psychotherapy Tp1", intake_pt_tp1, dry_pt_tp1, saline_pt_tp1,
              vm_react_pt_tp1, webneuro_pt_tp1, mri_pt_tp1, tms_pt_tp1])
proc.add_row(["Psychotherapy Tp2", intake_pt_tp2, dry_pt_tp2, saline_pt_tp2,
              vm_react_pt_tp2, webneuro_pt_tp2, mri_pt_tp2, tms_pt_tp2])
proc.add_row(["Healthy Veterans", intake_hv, dry_hv_tp1,
              saline_hv_tp1, vm_react_hv, webneuro_hv, mri_hv, tms_hv])


table = PrettyTable()

table.field_names = ['-', 'Tp1 Completions',
                     'Tp2 Completions', '6 Month Followup']
table.add_row(["Psychotherapy", tp1_completed_patients,
               tp2_completed_patients, six_month_followup])
table.add_row(["Healthy Veterans", tp1_completed_hv, '-', '-'])
table.add_row(["EEG/fMRI Healthy Controls",
               tp1_completed_hc, tp2_completed_hc, '-'])

#
#print 'PT TP1 completed',tp1_completed_patients
#print 'PT TP2 completed',tp2_completed_patients
#print '6 month followup', six_month_followup
#print 'HV TP1 completed', tp1_completed_hv
#print 'HC TP1 completed', tp1_completed_hc
#print 'HC TP2 completed',tp2_completed_hc
#
#
#print 'pt tms',tms_pt
#print 'pt fmri',mri_pt
#print 'tp1 pt saline',saline_pt_tp1
#print 'pt dry tp1',dry_pt_tp1
#print 'hv dry',dry_hv_tp1
#print 'hv mri',mri_hv
#print 'hv saline',saline_hv_tp1
#print 'hc tp1 saline',saline_hc_tp1
#print 'tp2 pt saline',saline_pt_tp2

print(table)
print('')
print (proc)
#
