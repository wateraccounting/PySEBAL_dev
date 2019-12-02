# -*- coding: utf-8 -*-
"""
Created on Tue May 03 13:12:18 2016

@author: tih
"""

import SEBAL

inputExcel = r"D:\PySebal\SEBAL-master_3.3.7.1\SEBAL-master\SEBAL\InputEXCEL_v3_3_7_probav.xlsx"

for number in range(2,3):
    try:
		print 'starting line num: %d' % number
        SEBAL.SEBALcode(number,inputExcel)
        print 'line num: %d done' % number
        
    except:
        print 'SEBAL did not run line %d fully' % number
        

