#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 20:41:35 2018

@author: dawlat_local
"""


import pycurl
import cStringIO
import datetime as dt
import time
import sys
import pandas
from itertools import groupby


report_test = '31113'

current_date = str(time.strftime('%Y/%m/%d'))


clinic_dict = {'1': 'Palo Alto', '2': 'San Jose VA', '3': 'Monterey VA', '4': 'New Mexico VA', '5': 'Menlo Park',
               '6': 'Fresno', '7': 'Livermore', '8': 'Stockton', '9': 'Modesto', '10': 'Mather', '98': 'Other'}

token = 'BE22B1E1DCECC4631C50A7EFC7911EE2'
url = 'https://redcap.stanford.edu/api/'


patient_buf = cStringIO.StringIO()
patient_tracker_data = {
    'token': token,
    'content': 'report',
    'format': 'csv',
    'report_id': report_test,
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'returnFormat': 'csv'
}
ch = pycurl.Curl()
ch.setopt(ch.URL, url)
ch.setopt(ch.HTTPPOST, patient_tracker_data.items())
ch.setopt(ch.WRITEFUNCTION, patient_buf.write)
ch.perform()
patient_report = patient_buf.getvalue()
ch.close()
patient_buf.close()

data_rep_pt = str(object=patient_report)
data_rep_pt = data_rep_pt.replace(' ', '_').replace(
    ', ', ' ').replace('record_id_redcap', 'id')
data_test_pt = [data_rep_pt]

data_rep = str(object=patient_report)
data_rep = data_rep.replace(' ', '_').replace(
    ', ', ' ').replace('record_id_redcap', 'id')
data_test = [data_rep]

patient_corrected_list = []
for test in data_test_pt:
    y = test.split()
    for idx, val in enumerate(y):
        patient_corrected_list.append(val.split(','))

df = pandas.DataFrame(data=patient_corrected_list)
column_headers = df[0:1].values.tolist()
df.columns = column_headers
df_corr_col_headers = df[1:]

#####


clinic = df_corr_col_headers.groupby('redcap_event_name')[
    'if_a_patient_which_va_clin'].value_counts()

s5_sched = df_corr_col_headers.groupby('redcap_event_name')[
    'session_5_followup'].value_counts()

s5_call = df_corr_col_headers.groupby('redcap_event_name')[
    'session_5_followup_call'].value_counts()

pt_therapy = df_corr_col_headers.groupby('redcap_event_name')[
    'if_a_patient_what_therapy_2'].value_counts()

therapy_completed = df_corr_col_headers.groupby(
    'redcap_event_name')['completed_all_therapy'].value_counts()

pt_dropped_therapy = df_corr_col_headers.groupby(
    'redcap_event_name')['why_therapy_not_completed___1'].value_counts()

pt_dropped_unreachable = df_corr_col_headers.groupby(
    'redcap_event_name')['why_therapy_not_completed___2'].value_counts()

pt_switched_modals = df_corr_col_headers.groupby(
    'redcap_event_name')['why_therapy_not_completed___3'].value_counts()

pt_dropped_other = df_corr_col_headers.groupby(
    'redcap_event_name')['why_therapy_not_completed___98'].value_counts()

tp1_sched = df_corr_col_headers.groupby('redcap_event_name')[
    'is_the_participant_confirm'].value_counts()

tp2_sched = df_corr_col_headers.groupby('redcap_event_name')[
    'is_the_participant_co2_2e3'].value_counts()

tp1_complete = df_corr_col_headers.groupby('redcap_event_name')[
    'time_point_completion_master'].value_counts()

tp2_complete = df_corr_col_headers.groupby('redcap_event_name')[
    'time_point_completion_master1'].value_counts()

eligibile = df_corr_col_headers.groupby('redcap_event_name')[
    'is_the_subject_eligable'].value_counts()

ineligible_post_intake = df_corr_col_headers.groupby(
    'redcap_event_name')['qc_ineligbile_screen_3'].value_counts()

eligible_post_intake = df_corr_col_headers.groupby(
    'redcap_event_name')['qc_eligbile_screen_2'].value_counts()

withdrawn_withdrew = df_corr_col_headers.groupby(
    'redcap_event_name')['qc_withdrew_status'].value_counts()

eligibility_screen = df_corr_col_headers.groupby(
    'redcap_event_name')['qc_eligbile_screen'].value_counts()

screen_comp_status = df_corr_col_headers.groupby(
    'redcap_event_name')['has_the_participant_comple'].value_counts()


print "Total Tp1 completions", tp1_complete[1]
print "Total Tp2 completions", tp2_complete[1]
print "Patients pending online screen completions", screen_comp_status.loc[
    'tp1_day1_arm_1'][2]


print ''
print "Total recieving PE:", tp1_sched.loc['tp1_day1_arm_1'][1] - \
    pt_therapy[2], "/", tp1_complete[1]
# DETERMINE IF WE INCLUDE PPL WHO HAVENT COPLETED TP1 YET

print "Total recieving CPT:", pt_therapy[1] - \
    (tp1_sched.loc['tp1_day1_arm_1'][3]), "/", tp1_complete[1]

print "Type of therapy still undecided:", pt_therapy[3], "/", tp1_complete[1]

print "Total recieving other form of therapy (Not CPT or PE):", pt_therapy[
    4], "/", tp1_complete[1]
print ''


print "total completed S5 call", s5_sched.loc['tp1_day1_arm_1'][
    1], "/", s5_sched.loc['tp1_day1_arm_1'][2] + s5_sched.loc['tp1_day1_arm_1'][1]

print "ready for S5 call:", s5_sched.loc['tp1_day1_arm_1'][3]
print ''

# NEED OT FIX:
print "Completed Tp1- Treatment in progress:", tp1_complete.loc['tp1_day1_arm_1'][1] - \
    therapy_completed[1] - therapy_completed[2] - tp2_sched[2]

print "Completed Treatment- Tp2 scheduling in progress:", tp2_sched.loc[
    'tp1_day1_arm_1'][2] - tp2_sched.loc['tp1_day1_arm_1'][3]

print "Completed Treatment- Tp2 scheduled:", tp2_sched.loc['tp1_day1_arm_1'][1] - \
    tp2_complete.loc['tp1_day1_arm_1'][1] - tp2_sched.loc['tp1_day1_arm_1'][3]

print ''

print "Total dropped out of treatmnet:", pt_dropped_therapy.loc['tp1_day1_arm_1'][1] + \
    pt_dropped_unreachable.loc['tp1_day1_arm_1'][1] + \
    pt_switched_modals.loc['tp1_day1_arm_1'][1]

print "Dropped out of Treatment- Collected Tp2 clinical measures:", tp2_complete[2]
print "Dropped out of Treatment- Collected Tp2 Data:",
print "Dropped out of Treatment- No Tp2 Data", tp2_complete[2]
print "Withdrawn or Withdrew:", withdrawn_withdrew.loc['tp1_day1_arm_1'][1]
