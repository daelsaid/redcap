#Redcap 

 #!/usr/bin/env python
import pycurl, cStringIO
import string
import collections
import time
from itertools import groupby


patient_buf = cStringIO.StringIO()
patient_tracker_data = {
    'token': 'BE22B1E1DCECC4631C50A7EFC7911EE2',
    'content': 'report',
    'format': 'csv',
    'report_id': '20886',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'returnFormat': 'csv'
    }
ch = pycurl.Curl()
ch.setopt(ch.URL, 'https://redcap.stanford.edu/api/')
ch.setopt(ch.HTTPPOST, patient_tracker_data.items())
ch.setopt(ch.WRITEFUNCTION, patient_buf.write)
ch.perform()
patient_report=patient_buf.getvalue()
ch.close()
patient_buf.close()


buf = cStringIO.StringIO()
data = {
    'token': 'BE22B1E1DCECC4631C50A7EFC7911EE2',
    'content': 'report',
    'format': 'csv',
    'report_id': '20560',
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
report=buf.getvalue()
ch.close()
buf.close()


data_rep_pt = str(object=patient_report) #patient specific report
data_rep_pt = data_rep_pt.replace(' ', '_')
data_rep_pt = data_rep_pt.replace('record_id_redcap', 'id')
data_rep_pt = data_rep_pt.replace(', ', ' ')
data_test_pt = [data_rep_pt]

data_rep = str(object=report) 
data_rep = data_rep.replace(' ', '_')
data_rep = data_rep.replace('record_id_redcap', 'id')
data_rep = data_rep.replace(', ', ' ')
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


current_date= str(time.strftime('%Y/%m/%d'))
clinic_dict = {'1': 'Palo Alto' , '2': 'San Jose VA', '3': 'Monterrey VA', '4': 'New Mexico VA', '5': 'Menlo Park',
               '6': 'Fresno', '7': 'Livermore' }



patient_referrals=0
referall_date=0
ineligible_patients_recruitment=0
total_patients_scheduled = 0
patients_pending_eligibility=0
number_in_process_of_being_scheduled=0
pending_eligibility_locations=[]
total_eligible_referrals=0
freq_of_referrals=[]

scheduled_patient_tp1=0
referred_patient_tp1=0
completed_patient_tp1=0
total_subj_with_data_collected=0
pt_weekly_count=0
pt_upcoming_dates=[]

total_hc_tp1_scheduled=0
total_hc_tp2_scheduled=0
completed_hc_tp1=0
completed_hc_tp2=0
weekly_count=0
weekly_count_tp2=0

total_hc_tp2_complete =0
total_hc_tp1_complete = 0
total_run_subjects=0



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
    if '55' in pt[5]:
        clinic = pt[6]
        try:
            clinic_type = clinic_dict[clinic]
        except:
            subj=pt[0]
            print "subject %s's clinic referral location field is empty, please fix this on redcap" %subj
            continue
        pending_eligibility_locations.append(clinic_type)
        patients_pending_eligibility = patients_pending_eligibility + 1
    if '0' in pt[5]:
        ineligible_patients_recruitment = ineligible_patients_recruitment + 1
    if '1' in pt[5]:
        total_eligible_referrals= total_eligible_referrals + 1
        clinics= clinic_dict[pt[6]]
        freq_of_referrals.append(clinics)
        
    
referrals_freqs= [(k,len(list(g))) for k, g in groupby(sorted(freq_of_referrals))]
pending_eligibility=[(k,len(list(g))) for k, g in groupby(sorted(pending_eligibility_locations))]


for subjects in corrected_list:
    subjects[9] = subjects[9].replace('-', '/')
    subjects[10] = subjects[10].replace('-', '/')
    if 'tp1_day1_arm_1' in subjects[1]:
        scheduled=[]
        referred=[]
        completed=[]
        total_run=[]
        total_subj_with_data=[]
        subj=subjects[0:]
        scheduled = subjects[3].count('1')
        scheduled_patient_tp1 = scheduled_patient_tp1 + scheduled
        completed = subjects[5].count('1')
        completed_patient_tp1 = completed_patient_tp1 + completed
        total_subj_with_data = subjects[11].count('1')
        total_subj_with_data_collected = total_subj_with_data_collected + total_subj_with_data
        pt_dates= subj[9]
        pt_count=0        
        if current_date <= pt_dates:
            pt_count += 1
            pt_weekly_count= pt_weekly_count + pt_count
            patient_upcoming_appt_date= pt_dates 
            pt_upcoming_dates.append(patient_upcoming_appt_date)
        else:
            total_run= subjects[9].count('1')
            total_run_subjects = total_run_subjects + total_run
    if 'arm_3' in subjects[1]:
        scheduled=[]
        weekly=[]
        referred=[]
        tp1_completed=[]
        tp2_completed=[]
        subj=subjects[0:]
        #hc tp1 sched
        scheduled = subjects[3].count('1')
        total_hc_tp1_scheduled = total_hc_tp1_scheduled + scheduled
        #hc tp2 sched
        scheduled = subjects[5].count('1')
        total_hc_tp2_scheduled = total_hc_tp2_scheduled + scheduled
        #hc tp1 completed
        tp1_completed = subjects[5].count('1')
        total_hc_tp1_complete = total_hc_tp1_complete + tp1_completed
        #hc tp2 completed
        tp2_completed = subjects[6].count('1')
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
    upcoming_pt_dates.append(date)
    
upcoming_dates = '(' + upcoming_pt_dates[0] + ', ' + upcoming_pt_dates[1] + ', ' + upcoming_pt_dates[2] + ')'  



#output -----
print "Current Date: " + time.strftime('%Y/%m/%d')   ## Only date representation
print ""

print '~~Patient Numbers:'
print ''
print "Total referrals: %s" %patient_referrals
print "Total number of eligible patients (upon referral): %s" %total_eligible_referrals
print ''

for ref in referrals_freqs:
    print ref
print ''
print "Total number of ineligible patients: %s" %ineligible_patients_recruitment 
print "Patients still pending eligibility (haven't completed online screen yet): %s" %patients_pending_eligibility
print ''
for pending in pending_eligibility:
    print pending
print ''
print "Total patients scheduled for Tp1: %s" %scheduled_patient_tp1
print "Total number of signed consent forms: %s" %total_subj_with_data_collected
print "Number of Tp1 completions: %s" %completed_patient_tp1 
print "Total upcoming Tp1 appointments (as of today): %s" %pt_weekly_count
print ''
print upcoming_dates
print ''
print ''

print '~~HC Numbers:'
print ''
print "Total Tp1 completions: %s" %total_hc_tp1_complete
print "Total Tp2 completions: %s" %total_hc_tp2_complete
print "Total number scheduled for tp1: %s" %total_hc_tp1_scheduled
print "Total number scheduled for tp2: %s" %total_hc_tp2_scheduled
print "Total upcoming Tp1 appointments (as of today's date): %s" %weekly_count
print "Total upcoming Tp2 appointments (as of today's date): %s" %weekly_count_tp2
