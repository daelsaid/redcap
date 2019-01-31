import pandas as pd
import os

prefix='/Users/daelsaid/Desktop/scsnl_scratch/second_contact' #parent_folder
pids_to_contact_csv_name='pids_to_contact.csv' #csv with record IDs, column1 = record_id, column2= to_contact
redcap_data_export_with_contact_info='contactinfo.csv' #raw data export from redcap "second_reachout_data_export", report #48007
master_phone_screen_csv='master.csv' #phone screen that was merged with participant tracker that exists on box


#read CSVs
piled_record_ids=pd.read_csv(os.path.join(prefix,pids_to_contact_csv_name),dtype=str) #specific IDs with column for to contact
redcap_contact_info_report=pd.read_csv(os.path.join(prefix,redcap_data_export_with_contact_info),dtype=str) #data_export_rc
master_csv=pd.read_csv(os.path.join(prefix,master_phone_screen_csv),dtype=str) #phone screen

#pull relevant fields from intake survey required for email trigering and remove duplicated rows (for now)
subset_of_contact_info=pd.DataFrame(data=redcap_contact_info_report[['record_id','email','firstname_parent','firstname_child']], dtype=str).drop_duplicates(subset='record_id',keep='first')

#pull the relevant fields from the repeating instrument
assignment_with_status=pd.DataFrame(data=redcap_contact_info_report[['record_id','study_assignment','study_assignment_status']],dtype=str)

#merge to create a csv file reflecting redcap repeating instruments format
subset_of_contact_info.merge(assignment_with_status,on='record_id',how='outer',copy=False).to_csv(os.path.join(prefix,'01_formatted_for_redcap_data_import.csv'))

#create csv file with 1 line per subject and merge their contact info with study assignment
study_assignment_and_status=pd.DataFrame(data=redcap_contact_info_report[['record_id','study_assignment','study_assignment_status']],dtype=str).drop_duplicates(subset='record_id',keep='last')

#create new df that has the merged contactt info and assignment status in 1 row
single_row_per_record_df=pd.DataFrame(data=subset_of_contact_info.merge(study_assignment_and_status,on='record_id',how='outer',copy=False))

#merge study_assignment_and_status that has no duplicated record IDs and the subset of contact info initialized above (duplicates have been dropped)
single_row_per_subj=pd.DataFrame(data=single_row_per_record_df.merge(study_assignment_and_status,on='record_id',how='outer',copy=False))

#write to csv
single_row_per_subj.to_csv(os.path.join(prefix,'01_single_row_per_subject.csv'))

##merge single_row_per_subj with master phone screen data and participant_tracker and create column that lists where each subject record was merged from
#left= from redcap
#right = from master phone screen + participant_tracker
final=pd.DataFrame(data=single_row_per_subj.merge(master_csv,left_on='record_id', right_on='record_id',how='outer',indicator=True),dtype=str).drop_duplicates(subset='record_id',keep='first')

#write this merged tracker to csv
final.to_csv(os.path.join(prefix,'merged_master_participant_tracker.csv'))
