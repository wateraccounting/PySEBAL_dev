# -*- coding: utf-8 -*-
"""
Created on Tue May 03 13:12:18 2016

@author: tih
"""

import pysebal_py2
# For Linux
# inputExcel = r"/mnt/d/PySebal/PySEBAL_Pareeth/PySEBAL_dev/docs/InputEXCEL_v3_3_7_LIN.xlsx"
# For Windows
inputExcel = r"D:\PySebal\PySEBAL_Pareeth\PySEBAL_dev\docs\InputEXCEL_v3_3_7_WIN.xlsx"

for number in range(2,3):
    try:
        print 'starting line num: %d' % number
        pysebal_py2.SEBALcode(number,inputExcel)
        print 'line num: %d done' % number
        
    except:
        print 'SEBAL did not run line %d fully' % number
        

