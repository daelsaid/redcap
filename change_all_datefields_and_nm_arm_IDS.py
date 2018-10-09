#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 19:18:33 2018

@author: dawlat_local
"""

from redcap import Project, RedcapError

api_url_best = ''
api_key_best = ''
best_project = Project(api_url_best, api_key_best)

api_url_screen =  ''
api_key_screen = ''
screen_project = Project(api_url_screen, api_key_screen)

best_project.import_records(testing_df, overwrite='normal', format='df',return_format='json',return_content='count')

df=best_project.export_records(event_name='unique',events=['new_mexico_87108_t_arm_7','new_mexico_87108_t_arm_7'],fields=['record_id_redcap'],forms='participant_reachout_recruitment',format='df')

ser=df.index.to_series()
ser.values[0:,][0]
for i,record in df.groupby(level=[0,1]):
    print record.index.tolist()[0]

print df.index.tolist()[0]
data_dict=best_project.export_metadata(format='df')
data_dict.head()

datefields=data_dict.loc[data_dict['text_validation_type_or_show_slider_number']== 'date_dmy']

datefields["text_validation_type_or_show_slider_number"]='date_mdy'

data_dict.merge(data_dict.text_validation_type_or_show_slider_number)


print data_dict.head()
comb.to_csv(~)
variables=datefields.index.tolist()

all_dates=best_project.export_records(fields=variables,format='df')

all_dates["dates"]='date_mdy'
