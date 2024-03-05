# -*- coding: utf-8 -*-
"""
Created on 03 Dec 2019

@author: tih, sajid pareeth
"""

import pysebal_py3
import traceback # amir

##### USER INPUTS

##### For Linux SET THE PATH TO INPUT EXCEL SHEET #####
#inputExcel = r"/mnt/d/PySEBAL_dev/test_data/InputEXCEL_v3_3_7_LIN.xlsx"
##### For Windows SET THE PATH TO INPUT EXCEL SHEET #####
inputExcel = r"D:\testing_folder\datas\InputEXCEL_v3_3_7_part2.xlsx"
st = 2 # starting row number
en = 2 # ending row number

####### USER INPUTS FINISH HERE

for number in range(st, en + 1):
    try:
        print ('starting line num: %d' % number)
        pysebal_py3.SEBALcode(number,inputExcel)
        print ('line num: %d done' % number)   
    except:  # amir
        print ('--------------------\n')
        print ('SEBAL did not run line %d fully' % number)
        print ('\n******* ERROR *******\n')
        traceback.print_exc()
        
        print ('\n--------------------\n')        
