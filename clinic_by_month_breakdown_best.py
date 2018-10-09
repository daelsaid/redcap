#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 00:44:47 2018

@author: dawlat_local
"""
import pandas

csv_stuff=pandas.read_csv('')

print csv_stuff.count()
csv=pandas.DataFrame(data=csv_stuff.set_index('clinic_referral'))

for x,y in csv.groupby(level=0):
    print x,y['date'].value_counts()
    print x,y
    print x.index, y.tolist().value_counts()
