#Redcap

 #!/usr/bin/env python
import pycurl, cStringIO
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

current_date= str(time.strftime('%Y/%m/%d'))
clinic_dict = {'1': 'Palo Alto' , '2': 'San Jose VA', '3': 'Monterey VA', '4': 'New Mexico VA', '5': 'Menlo Park',
               '6': 'Fresno', '7': 'Livermore', '8': 'Stockton', '98': 'Other'}

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

pt_cpt_therapy=0
pt_therapy_still_unknown=0
pt_pe_therapy=0
dropped=0
ready_tp2=0
flwup=0

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
hv_tp1_sched=0

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
        pt_count=0
        if current_date <= pt_dates:
            pt_count += 1
            pt_weekly_count= pt_weekly_count + pt_count
            patient_upcoming_appt_date= pt_dates
            pt_upcoming_dates.append(patient_upcoming_appt_date)
        else:
            total_run= subjects[9].count('1')
            total_run_subjects = total_run_subjects + total_run
    if 'arm_2' in subjects[1]:
        subj_all=subjects[0:]
        if subj_all[12] == '50':
            hv_pending_screen = hv_pending_screen + 1
        if subj_all[3] == '1':
            hv_tp1_sched= hv_tp1_sched + 1
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


#output -----
print "Current Date: " + time.strftime('%Y/%m/%d')   ## Only date representation
print ""

print '~~Patient Numbers:'
print ''
print "Total referrals: %s" %patient_referrals
#print 'Total number of sent interest cards %s' %total_interest_cards
print "Total number of eligible patients (upon referral/online screen): %s" %total_eligible_referrals
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
print "Total Number of patients we have data for (Pt who have consented): %s" %total_subj_with_data_collected
print "Total Number of Tp1 completions: %s" %completed_patient_tp1
print "Total upcoming Tp1 appointments (as of today's date): %s" %pt_weekly_count
print ''
for pt_date in upcoming_pt_dates:
    print pt_date
print ''
print ''

print "Total Number of patients receiving CPT: %s" %pt_cpt_therapy
print "Total Number of patients receiving PE therapy: %s" %pt_pe_therapy
print "Number of patients that are still deciding between CPT and PE: %s" %pt_therapy_still_unknown
print ''

print "Number of patients ready for Session 5 Follow-Up Calls: %s" %flwup
print "Number of patients that have completed therapy: %s" %completed_all_therapy
print "Number of patients that dropped out of therapy: %s" %dropped
print ''

print "Number of patients ready to be scheduled for Tp2: %s" %ready_tp2
print "Number of patients in process of being scheduled for Tp2: %s" %in_process_tp2
print "Total patients scheduled for Tp2: %s" %sched_tp2
print "Total Number of Tp2 completions: %s" %completed_patient_tp2
print ''

print '~~Healthy Veteran Numbers:'
print ''
print 'Vets pending online screen completion: %s' %hv_pending_screen
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
