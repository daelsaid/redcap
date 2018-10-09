
"""
Created on Sat Jun  9 19:18:33 2018

@author: dawlat_local
"""

from redcap import Project, RedcapError
import pandas

api_url_best = 'https://redcap.stanford.edu/api/'
api_key_best = ''
best_project = Project(api_url_best, api_key_best)

api_url_screen = 'https://redcap.stanford.edu/api/'
api_key_screen = ''
os = Project(api_url_screen, api_key_screen)


best_rc_df = best_project.export_records(event_name='unique', events=['tp1_day1_arm_1'], fields=['record_id_redcap'], forms=[
                                         'participant_reachout_recruitment', 'best_master', 'consent', 'online_screening_survey'], format='df', df_kwargs={'dtype': 'str'})
os_rc_df = os.export_records(event_name='unique', fields=['OnlineID'], forms=[
                             'final_determination', 'demographics_and_background', 'online_screening_survey'], format='df', df_kwargs={'dtype': 'str'})


best_columns = ['record_id_redcap', 'redcap_id_main', 'is_the_subject_eligable', 'eligibility_referral_master___0', 'eligibility_referral_master___1', 'reason_for_ineligbility', 'enrollment_status___3', 'enrollment_status___2', 'enrollment_status___1', 'ineligible_reason', 'time_point_completion_master', 'time_point_completion_master1', 'enrolled_for', 'has_the_participant_comple', 'interest_card_sent', 'interest_card_sent_by','date_the_interest_card_was', 'redcap_id_main', 'reach_out_first_name', 'middle_name_optional', 'reachout_last_name', 'dob_reachout', 'current_age', 'consent_age', 'email_sr_surveys', 'phone_number_reach', 'phone_number_secondary', 'age_dob', 'gender', 'race___1', 'race___2', 'race___3', 'race___4', 'race___5', 'race___6', 'ethnicity', 'gender', 'stanford_consent_completed', 'va_consent_completed', 'stanford_consent_comp2_6ae']

os_columns = ['record_id_redcap', 'redcap_event_name', 'redcap_repeat_instrument_x', 'redcap_repeat_instance_x', 'enrolled_for', 'if_other_what_is_the_subje', 'has_the_participant_comple', 'interest_card_sent', 'interest_card_sent_by', 'date_the_interest_card_was', 'redcap_id_main', 'reach_out_first_name', 'middle_name_optional', 'reachout_last_name', 'eligibility_referral_master___0', 'eligibility_referral_master___1', 'who_det_eligibility_master', 'who_confirmed_eligibility', 'reason_for_ineligbility','enrollment_status___3', 'enrollment_status___2', 'enrollment_status___1', 'enrollment_withdraw', 'ineligible_reason', 'who_confirmed_eligibility_2', 'time_point_completion_master','all_study_2', 'study_appointments_complet___1', 'study_appointments_complet___15', 'study_appointments_complet___2', 'study_appointments_complet___18', 'study_appointments_complet___19',  'stanford_consent_completed', 'va_consent_completed', 'stanford_consent_comp2_6ae', 'date_of_consent', 'online_id',  'referral', 'referral_other', 'first_name', 'last_name', 'email', 'phone_1', 'phone_2',  'online_notes', 'demo_best_notes', 'demographics_and_background_complete', 'agree_participate_y', 'date_y', 'age_y', 'age_dob_y', 'gender_y', 'race___2_y', 'race___3_y', 'race___4_y', 'race___5_y', 'race___6_y', 'ethnicity_y', 'vet_y', 'study_refer', 'referral_date_y', 'study_referral']

c = ['record_id_redcap', 'enrolled_for', 'eligibility_referral_master___0', 'eligibility_referral_master___1', 'who_det_eligibility_master', 'who_confirmed_eligibility','reason_for_ineligbility', 'enrollment_status___3', 'enrollment_status___2', 'enrollment_status___1', 'enrollment_withdraw', 'ineligible_reason', 'who_confirmed_eligibility_2']

race = ['race___1', 'race___2', 'race___3', 'race___4', 'race___5', 'race___6']


merged = best_rc_df.merge(os_rc_df.reset_index(
), left_on='redcap_id_main', right_on='online_id', how='left', copy=False)
merged_cols = mergebest_rc_df.columns.tolist()


merged_best_columns = []
for x in merged_cols:
    merged_best_columns.append(x.split('_x')[0:2])

merged_best_columns = [x for x in merged_best_columns]

for x, y in best_rc_df[c].groupby('enrolled_for'):
    y.to_csv('eligibility.csv')

for x, y in mergebest_rc_df.groupby('gender_y')[os_columns]:
    testing = pbest_rc_df.DataFrame()
    if any((y['va_consent_completed'].values == '1')) or any((y['stanford_consent_completed'].values == '1')):
        print y['record_id_redcap'].values.tolist()[0:][0:]
        print y['stanford_consent_completed'].values.tolist()[0:][0:]
        print y['va_consent_completed'].values.tolist()[0:][0:]
    for r in race:
        if any((y['study_referral'].values == '9')) or any((y['study_referral'].values == '10')):
            print y[r + '_y'].values.tolist()[0:][0:]
            print y['record_id_redcap'].values.tolist()[0:][0:]
            print y['ethnicity_y'].values.tolist()[0:][0:]
    if x == '0':
        print 'female'
        print x
        if (y['va_consent_completed'].values == '1').any() or (y['stanford_consent_completed'].values == '1').any():
            print y.count()
            print y['va_consent_completed'].value_counts()
            print y['stanford_consent_completed'].value_counts()
            print '*****'
            print '**American Indian or Alaska Native:'
            print y['race___1_y'].value_counts()
            print '**Asian'
            print y['race___2_y'].value_counts()
            print '**Black or African American'
            print y['race___3_y'].value_counts()
            print '**Native Hawaiian or Other Pacific Islander'
            print y['race___4_y'].value_counts()
            print '**White'
            print y['race___5_y'].value_counts()
            print '**Other'
            print y['race___6_y'].value_counts()
    elif x == '1':
        if (y['va_consent_completed'].values == '1').any() or (y['stanford_consent_completed'].values == '1').any():
            print y.count()
            print 'male'
            print y['va_consent_completed'].value_counts()
            print y['stanford_consent_completed'].value_counts()
            print '**American Indian or Alaska Native:'
            print y['race___1_y'].value_counts()
            print '**Asian'
            print y['race___2_y'].value_counts()
            print '**Black or African American'
            print y['race___3_y'].value_counts()
            print '**Native Hawaiian or Other Pacific Islander'
            print y['race___4_y'].value_counts()
            print '**White'
            print y['race___5_y'].value_counts()
            print '**Other'
            print y['race___6_y'].value_counts()


for x, y in os_rc_df.groupby('study_referral')[os_columns]:
    if x == '0':
        print 'female'
        print y['va_consent_completed'].value_counts()
        print y['stanford_consent_completed'].value_counts()
        print 'American Indian or Alaska Native', y['race___1'].value_counts()
        print 'Asian', y['race___2'].value_counts()
        print 'Black or African American', y['race___3'].value_counts()
        print 'Native Hawaiian or Other Pacific Islander', y['race___4'].value_counts(
        )
        print 'White', y['race___5'].value_counts()
        print 'Other', y['race___6'].value_counts()
    else:
        y.count()
        print 'male'
        print y['va_consent_completed'].value_counts()
        print y['stanford_consent_completed'].value_counts()
        print 'American Indian or Alaska Native', y['race___1'].value_counts()
        print 'Asian', y['race___2'].value_counts()
        print 'Black or African American', y['race___3'].value_counts()
        print 'Native Hawaiian or Other Pacific Islander', y['race___4'].value_counts(
        )
        print 'White', y['race___5'].value_counts()
        print 'Other', y['race___6'].value_counts()
