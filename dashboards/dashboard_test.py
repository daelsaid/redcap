#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 17:58:50 2017

@author: dawlat_local
"""


"""
Spyder Editor
"""
import pycurl, cStringIO
import datetime as dt
import time
import sys
import pandas
from itertools import groupby


report_test='28266'




current_date= str(time.strftime('%Y/%m/%d'))
meeting_date=sys.argv[0]
#date_to_use_for_week=(datetime.datetime.now() - datetime.timedelta(days=sys.argv[1])).date()

clinic_dict = {'1': 'Palo Alto', '2': 'San Jose VA', '3': 'Monterey VA', '4': 'New Mexico VA', '5': 'Menlo Park', '6': 'Fresno', '7': 'Livermore', '8': 'Stockton', '9': 'Modesto','10': 'Mather', '98': 'Other'}

token='BE22B1E1DCECC4631C50A7EFC7911EE2'
url='https://redcap.stanford.edu/api/'


patient_buf = cStringIO.StringIO()
patient_tracker_data = {
    'token': token,
    'content': 'report',
    'format': 'csv',
    'report_id': '20886',
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
patient_report=patient_buf.getvalue()
ch.close()
patient_buf.close()




buf = cStringIO.StringIO()
data = {
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
ch.setopt(ch.HTTPPOST, data.items())
ch.setopt(ch.WRITEFUNCTION, buf.write)
ch.perform()
report=buf.getvalue()
ch.close()
buf.close()

data_rep_pt = str(object=patient_report) #patient specific report
data_rep_pt = data_rep_pt.replace(' ', '_').replace(', ', ' ').replace('record_id_redcap', 'id')
data_test_pt = [data_rep_pt]

data_rep = str(object=report)
data_rep = data_rep.replace(' ', '_').replace(', ', ' ').replace('record_id_redcap', 'id')
data_test = [data_rep]

patient_corrected_list=[]
for test in data_test_pt:
    y = test.split()
    for idx,val in enumerate(y):
        patient_corrected_list.append(val.split(','))

corrected_list=[]
for test in data_test:
    y = test.split()
    for idx,val in enumerate(y):
        corrected_list.append(val.split(','))



patient_df=pandas.DataFrame(data=patient_corrected_list)
length_of_data_frame=len(patient_df)


patient_column_headers=patient_df[0:1].values.tolist()
patient_df.columns=patient_column_headers
patient_report_df=patient_df[1:]

general_dash=pandas.DataFrame(data=corrected_list)

general_dash_headers=general_dash[0:1].values.tolist()
general_dash.columns=general_dash_headers
general_dash_df=general_dash[1:]



test=patient_report_df['session_5_followup'].value_counts()



patient_referrals=0
referall_date=0
ineligible_patients_recruitment=0
total_patients_scheduled = 0
patients_pending_eligibility=0
number_in_process_of_being_scheduled=0
pending_eligibility_locations=[]
total_eligible_referrals=0
total_interest_cards=0
freq_of_referrals=[]

first_apt_therapy=0
scheduled_for_apt_1=0
first_apt_not_sched=0
pt_cpt_therapy=0
pt_therapy_still_unknown=0
pt_pe_therapy=0
dropped=0
ready_tp2=0
flwup=0
s2=0
s5=0
s10=0

scheduled_patient_tp1=0
referred_patient_tp1=0
completed_patient_tp1=0
scheduled_patient_tp2=0
referred_patient_tp2=0
completed_patient_tp2=0
sched_tp2=0
in_process_tp2 = 0

total_subj_with_data_collected=0
pt_weekly_count=0
pt_upcoming_dates=[]

hv_pending_screen=0
hv_completed_screen=0
hv_tp1_sched=0
hv_process_tp1=0

total_hc_tp1_scheduled=0
total_hc_tp2_scheduled=0
completed_hc_tp1=0
completed_hc_tp2=0
weekly_count=0
weekly_count_tp2=0

total_hc_tp2_complete =0
total_hc_tp1_complete = 0
total_run_subjects=0
completed_all_therapy=0
hv_tp1_upcoming_dates=[]
hv_tp2_upcoming_dates=[]
pt_tp2_upcoming_dates=[]
total_intakes_sched=0
upcoming_hv_intakes=0

for pt in patient_corrected_list:
    pt[3] = pt[3].replace('-', '/')
    referred =[]
    eligibility_recruitment=[]
    count =0
    if ' ' not in pt[3]:
        count +=1
        patient_referrals= patient_referrals + 1
    else:
        continue
    if '1' in pt[11]:
        total_interest_cards = total_interest_cards + 1
    if '55' in pt[5]:
        clinic = pt[6]
        clinic_type = clinic_dict[clinic]
        pending_eligibility_locations.append(clinic_type)
        patients_pending_eligibility = patients_pending_eligibility + 1
    if '0' in pt[5]:
        ineligible_patients_recruitment = ineligible_patients_recruitment + 1
    if '1' in pt[5]:
        total_eligible_referrals= total_eligible_referrals + 1
        clinics= clinic_dict[pt[6]]
        freq_of_referrals.append(clinics)
    if '2' in pt[8] and pt[5] !='0' and pt[5] != '':
        pt_cpt_therapy= pt_cpt_therapy + 1
    if '100' in pt[8] and pt[5] !='0' and pt[5] != '':
        pt_therapy_still_unknown = pt_therapy_still_unknown + 1
    if '1' in pt[8] and pt[5] !='0' and pt[5] != '':
        pt_pe_therapy = pt_pe_therapy + 1
    if '1' in pt[9] and '1' not in pt[10]:
        sched_tp2=sched_tp2+1
    if '1' in pt[9] and '1' in pt[10]:
        completed_patient_tp2=completed_patient_tp2 + 1
    if pt[9] == '55':
        in_process_tp2=in_process_tp2+1
    if pt[12] == '1':
        completed_all_therapy=completed_all_therapy + 1
    if pt[12] == '0':
        dropped = dropped +1
    if pt[14] == '55':
        flwup=flwup + 1
    if pt[16] == '1' and pt[17] != '0':
        ready_tp2=ready_tp2 + 1
    if pt[13] == '1':
        s2=s2 + 1
    if pt[14] == '1':
        s5=s5 + 1
    if pt[15] == '1':
        s10=s10 + 1
    if pt[18] == '1' and pt[20] == '1':
        first_apt_therapy=first_apt_therapy + 1
    if pt[18] == '0' and pt[19] != '' and pt[20] == '1' :
        scheduled_for_apt_1 = scheduled_for_apt_1 + 1
    if pt[18] == '0' and pt[19] == '' and pt[20] == '1' :
        first_apt_not_sched=first_apt_not_sched+1



referrals_freqs= [(k,len(list(g))) for k, g in groupby(sorted(freq_of_referrals))]
pending_eligibility=[(k,len(list(g))) for k, g in groupby(sorted(pending_eligibility_locations))]

for subjects in corrected_list:
    subjects[9] = subjects[9].replace('-', '/')
    subjects[10] = subjects[10].replace('-', '/')
    if 'tp1_day1_arm_1' in subjects[1]:
        scheduled=[]
        tp2_scheduled=[]
        referred=[]
        completed_tp1=[]
        completed_tp2=[]
        total_run=[]
        total_subj_with_data=[]
        subj=subjects[0:]
        scheduled = subjects[3].count('1')
        scheduled_patient_tp1 = scheduled_patient_tp1 + scheduled
        completed_tp1 = subjects[5].count('1')
        completed_patient_tp1 = completed_patient_tp1 + completed_tp1
        tp2_sched_temp = subjects[4].count('1')
        total_subj_with_data = subjects[11].count('1')
        total_subj_with_data_collected = total_subj_with_data_collected + total_subj_with_data
        pt_dates= subj[9]
        tp2dates=subj[10]
        pt_count=0
        if current_date <= pt_dates:
            pt_count += 1
            pt_weekly_count= pt_weekly_count + pt_count
            patient_upcoming_appt_date= pt_dates
            pt_upcoming_dates.append(patient_upcoming_appt_date)
        else:
            total_run= subjects[9].count('1')
            total_run_subjects = total_run_subjects + total_run
        if current_date <= tp2dates:
            pt_tp2_upcoming_dates.append(tp2dates)
    if 'arm_2' in subjects[1]:
        subj_all=subjects[0:]
        if subj_all[12] == '55':
            hv_pending_screen = hv_pending_screen + 1
        if subj_all[3] == '1' and subj_all[5] == '':
            hv_tp1_sched= hv_tp1_sched + 1
        if subj_all[3] == '55':
            hv_process_tp1 = hv_process_tp1 + 1
        hv_tp1_dates=subj_all[9]
        hv_tp1_count=0
        if current_date <= hv_tp1_dates:
            hv_tp1_count +=1
            hvtp1_upcoming_appt_date= hv_tp1_dates
            hv_tp1_upcoming_dates.append(hvtp1_upcoming_appt_date)
        total_intakes_sched = len(hv_tp1_dates)
        if hv_tp1_dates != '':
            total_intakes_sched = total_intakes_sched + 1
    if 'arm_3' in subjects[1]:
        scheduled=[]
        weekly=[]
        referred=[]
        tp1_completed=[]
        tp2_completed=[]
        subj=subjects[0:]
        scheduled = subjects[3].count('1')         #hc tp1 sched
        total_hc_tp1_scheduled = total_hc_tp1_scheduled + scheduled
        scheduled = subjects[5].count('1')         #hc tp2 sched
        total_hc_tp2_scheduled = total_hc_tp2_scheduled + scheduled
        tp1_completed = subjects[5].count('1')         #hc tp1 completed
        total_hc_tp1_complete = total_hc_tp1_complete + tp1_completed
        tp2_completed = subjects[6].count('1')         #hc tp2 completed
        total_hc_tp2_complete = total_hc_tp2_complete + tp2_completed
        scheduled = subjects[4].count('1')
        dates_tp1= subj[9]
        count=0
        if current_date <= dates_tp1:
            count += 1
            weekly_count= weekly_count + 1
        else:
            continue
        dates_tp2=subj[10]
        count_tp2=0
        if current_date <= dates_tp2:
            count_tp2 += 1
            weekly_count_tp2= weekly_count_tp2 + 1



pt_upcoming_dates = sorted(pt_upcoming_dates)

upcoming_pt_dates=[]
for date in pt_upcoming_dates:
    date = [date]
    upcoming_pt_dates.append(date)


hv_tp1_apt_dates=sorted(hv_tp1_upcoming_dates)


#output -----
print "Current Date: " + time.strftime('%Y/%m/%d')   ## Only date representation
print ""

print '~~Patients:'
print ''

print "Total Number of Tp1 completions: %s" %completed_patient_tp1 #NEED WEEK
print "Total Number of Tp2 completions: %s" %completed_patient_tp2 #NEED WEEK
print "Total referrals: %s" %patient_referrals
print "Total number of eligible patients (upon referral/online screen): %s" %total_eligible_referrals


print '~~Healthy Veterans:'
print ''

print 'Total number of healthy vet intakes scheduled: %s' %total_intakes_sched
print '**TOTAL HVs completed procedures'
print 'Healthy Vets pending online screen completion: %s' %hv_pending_screen

#print 'Total number of sent interest cards %s' %total_interest_cards
print ''



print '~~Healthy Controls:'
print ''
print "Total Tp1 completions: %s" %total_hc_tp1_complete #NEED WEEK
print "Total Tp2 completions: %s" %total_hc_tp2_complete
#REFERRALS/week


print 'Patient Recruitment Sites'
for ref in referrals_freqs:
    print ref


print ''

print 'Patient Specifics'
print ''

print "Number of patients ready for their Session 5 Follow-Up Call: %s" %flwup
print #SESSION 5 FOllowups that happened this week/total
print "Total Number of patients receiving CPT: %s" %pt_cpt_therapy
print "Total Number of patients receiving PE therapy: %s" %pt_pe_therapy
print "Number of patients that are still deciding between CPT and PE: %s" %pt_therapy_still_unknown
print "Total upcoming Tp1 appointments (As of Today's Date): %s" %pt_weekly_count
print "Number of patients ready to be scheduled for Tp2: %s" %ready_tp2
print "Number of patients actively in process of being scheduled for Tp2: %s" %in_process_tp2
print "Total patients scheduled for Tp1: %s" %scheduled_patient_tp1
print "Total patients scheduled for Tp2 (As of today's date): %s" %sched_tp2


print '~~Healthy Veterans'
print ''
print 'Healthy Vets that completed online screen: %s' %hv_completed_screen
print 'Healthy Vets in the process of being scheduled: %s' %hv_process_tp1
print 'Total upcoming healthy vet intakes scheduled (as of today\'s date): %s' %hv_tp1_sched
print ''


print '~~Healthy Controls:'
print "Total upcoming Tp1 appointments (as of today's date): %s" %weekly_count
print "Total upcoming Tp2 appointments (as of today's date): %s" %weekly_count_tp2


print ''
print 'Upcoming Appointment Dates'

print ''
print 'Patients:'
print ''
for pt_date in pt_upcoming_dates:
    print '['+pt_date +']'


print 'Healthy Veterans:'
print ''
for hvdate in hv_tp1_apt_dates:
    print '['+hvdate + ']'







print ''
print "Total number of ineligible patients: %s" %ineligible_patients_recruitment
print "Patients still pending eligibility (haven't completed online screen yet): %s" %patients_pending_eligibility
print ''
for pending in pending_eligibility:
    print pending


print ''
print "Total Number of patients we have data for (Pt who have consented): %s" %total_subj_with_data_collected
print ''

print ''

print ''


print 'Number of patients who have completed Tp1 and have started treatment: %s' %first_apt_therapy
print 'Number of patients who have completed Tp1 and not Treatment Session 1: %s' %first_apt_not_sched
print 'Number of patients who have completed Tp1 and have prospective dates for Treatment Session 1: %s' %scheduled_for_apt_1
print ''

print "Number of patients that have completed therapy: %s" %completed_all_therapy
print "Number of patients that dropped out of therapy: %s" %dropped
print ''
print ''




print ''

print ''

print "Total number scheduled for tp1: %s" %total_hc_tp1_scheduled
print "Total number scheduled for tp2: %s" %total_hc_tp2_scheduled


#-----


# #test_df=pandas.DataFrame(data=patient_corrected_list)
# length_of_data_frame=len(test_df)


# column_headers=test_df[0:1].values.tolist()
# test_df.columns=column_headers

# report_df=test_df[1:]

# print report_df

# report_df['session_5_followup'].value_counts()


# completed_patient_tp1


print "Current Date: " + time.strftime('%Y/%m/%d')   ## Only date representation
print ""

print '~~Patients:'
print "Tp1 completions this week:"
print "Tp2 completions this week:"
print "Total Referrals this week:"
print "Total Tp1 completions: %s" %completed_patient_tp1 #NEED WEEK
print "Total Tp2 completions: %s" %completed_patient_tp2 #NEED WEEK
print "Total referrals this week: %s" %patient_referrals #NEED WEEK
print "Total number of eligible patients (upon referral/online screen): %s" %total_eligible_referrals #OUT OF WEEK

print "Number of subjects we have collected data for:"


print ''

print '~~Healthy Veterans:'
print 'Number of healthy vet intakes scheduled: %s' %total_intakes_sched # OUT OF TOTAL
print 'Total number of HV completions'
print 'Healthy Vets pending online screen completion: %s' %hv_pending_screen

#print 'Total number of sent interest cards %s' %total_interest_cards
print ''



print '~~Healthy Controls:'
print "Total Tp1 completions this week:"
print "Total Tp2 completions this week:"
print "Referrals:"

#REFERRALS/week


print 'Patient Recruitment Site Numbers'
for ref in referrals_freqs:
	print ref

print ''

print 'Patient Specifics'
print ''

print "Number of patients ready for their Session 5 Follow-Up Call: %s" %flwup
print #SESSION 5 FOllowups that happened this week/total
print "Total Number of patients receiving CPT: %s" %pt_cpt_therapy
print "Total Number of patients receiving PE therapy: %s" %pt_pe_therapy
print "Number of patients still deciding between CPT and PE: %s" %pt_therapy_still_unknown
print "Total upcoming Tp1 appointments: %s" %pt_weekly_count
print "Number of patients ready to be scheduled for Tp2: %s" %ready_tp2
print "Number of patients actively in process of being scheduled for Tp2: %s" %in_process_tp2
print "Total patients scheduled for Tp1: %s" %scheduled_patient_tp1
print "Total patients scheduled for Tp2: %s" %sched_tp2


print '~~Healthy Veterans'
print ''
print 'Healthy Vets that completed online screen: %s' %hv_completed_screen
print 'Healthy Vets in the process of being scheduled: %s' %hv_process_tp1
print 'Total upcoming healthy vet intakes scheduled (as of today\'s date): %s' %hv_tp1_sched
print ''


print '~~Healthy Controls:'
print "Total Tp1 completions: %s" %total_hc_tp1_complete #NEED WEEK
print "Total Tp2 completions: %s" %total_hc_tp2_complete
print "Total upcoming Tp1 appointments: %s" %weekly_count
print "Total upcoming Tp2 appointments: %s" %weekly_count_tp2


print ''
print 'Upcoming Appointment Dates'

print ''
print 'Patient Tp1:'
print 'Patient Tp2:'

print ''
for pt_date in pt_upcoming_dates:
	print '['+pt_date +']'

print 'Healthy Veteran Intakes:'
for hvdate in hv_tp1_apt_dates:
	print '['+hvdate + ']'



# print "Current Date: " + time.strftime('%Y/%m/%d')   ## Only date representation
# print ""

# print '~~Patients:'
# print "Tp1 completions this week:"
# print "Tp2 completions this week:"
# print "Total Referrals this week:"
# print "Total Tp1 completions: %s" %completed_patient_tp1 #NEED WEEK
# print "Total Tp2 completions: %s" %completed_patient_tp2 #NEED WEEK
# print "Total referrals this week: %s" %patient_referrals #NEED WEEK
# print "Total number of eligible patients (upon referral/online screen): %s" %total_eligible_referrals #OUT OF WEEK

# print "Number of subjects we have collected data for:"


# print ''

# print '~~Healthy Veterans:'
# print 'Number of healthy vet intakes scheduled: %s' %total_intakes_sched # OUT OF TOTAL
# print 'Total number of HV completions'
# print 'Healthy Vets pending online screen completion: %s' %hv_pending_screen

# print 'Total number of sent interest cards %s' %total_interest_cards
# print ''



# print '~~Healthy Controls:'
# print "Total Tp1 completions this week:"
# print "Total Tp2 completions this week:"
# print "Referrals:"

# # #REFERRALS/week


# print 'Patient Recruitment Site Numbers'
# for ref in referrals_freqs:
#     print ref

# print ''

# print 'Patient Specifics'
# print ''

# print "Number of patients ready for their Session 5 Follow-Up Call: %s" %flwup
# print #SESSION 5 FOllowups that happened this week/total
# print "Total Number of patients receiving CPT: %s" %pt_cpt_therapy
# print "Total Number of patients receiving PE therapy: %s" %pt_pe_therapy
# print "Number of patients still deciding between CPT and PE: %s" %pt_therapy_still_unknown
# print "Total upcoming Tp1 appointments: %s" %pt_weekly_count
# print "Number of patients ready to be scheduled for Tp2: %s" %ready_tp2
# print "Number of patients actively in process of being scheduled for Tp2: %s" %in_process_tp2
# print "Total patients scheduled for Tp1: %s" %scheduled_patient_tp1
# print "Total patients scheduled for Tp2: %s" %sched_tp2


# print '~~Healthy Veterans'
# print ''
# print 'Healthy Vets that completed online screen: %s' %hv_completed_screen
# print 'Healthy Vets in the process of being scheduled: %s' %hv_process_tp1
# print 'Total upcoming healthy vet intakes scheduled (as of today\'s date): %s' %hv_tp1_sched
# print ''


# print '~~Healthy Controls:'
# print "Total Tp1 completions: %s" %total_hc_tp1_complete #NEED WEEK
# print "Total Tp2 completions: %s" %total_hc_tp2_complete
# print "Total upcoming Tp1 appointments: %s" %weekly_count
# print "Total upcoming Tp2 appointments: %s" %weekly_count_tp2


# print ''
# print 'Upcoming Appointment Dates'

# print ''
# print 'Patient Tp1:'
# print 'Patient Tp2:'

# print ''
# for pt_date in pt_upcoming_dates:
#     print '['+pt_date +']'

# print 'Healthy Veteran Intakes:'
# for hvdate in hv_tp1_apt_dates:
#     print '['+hvdate + ']'


#     ~~Patients:
# Total Number of Tp1 completions: 3
# Tp1 completions this week: 1
# Tp2 completions this week: 1
# Total referrals this week: 4/ 83
# Total  Tp2 completions: 9
# Total number of eligible patients (upon referral/online screen): 3/ 50

# ~~Healthy Veterans:
# Total number of Healthy Vet intakes scheduled: 3/ 11
# Total number of completions: 2
# Healthy Vets pending online screen completion: 0

# ~~Healthy Controls:
# Total Tp1 completions this week: 0/ 20
# Total Tp2 completions this week: 0/14
# Referrals: 0

# ~~Patient  Recruitment Site Numbers:
# Fresno: 0/ 4
# Livermore: 0/2
# Mather: 0/1
# Menlo Park: 0/ 6
# Modesto: 0/1
# Monterey VA: 0/ 4
# New Mexico VA: 1/ 20
# San Jose VA:  0/ 2


# ~~Patient Specifics
# Number of patients ready for their Session 5 Follow-Up Call: 3
# Total Number of patients receiving CPT: 21
# Total Number of patients receiving PE therapy: 17
# Number of patients that are still deciding between CPT and PE: 3
# Number of patients that have completed therapy: 12
# Number of patients that dropped out of therapy: 3
# Number of patients that completed Tp1 but are not doing PE or CPT: 2
# Total upcoming Tp1 appointments: 1
# Number of patients ready to be scheduled for Tp2: 3/13
# Number of patients actively in process of being scheduled for Tp2: 3
# Total patients scheduled for Tp1: 38
# Total patients scheduled for Tp2: 10

# ~~Healthy Veteran Specifics
# Healthy Vets that completed online screen this week: 0
# Healthy Vets in the process of being scheduled: 0
# Total upcoming Healthy Vet intakes scheduled: 5

# ~~Healthy Control Specifics
# Total upcoming Tp1 appointments:  0
# Total upcoming Tp2 appointments: 0

# Upcoming Appointment Dates
# Patient Tp1: 11/12/2017,
# Patient Tp2:  11/14/2017, 11/28/2017, 12/01/2017

# Healthy Veterans Intakes: 11/10/2017, 11/17/2017, 12/18/2017


