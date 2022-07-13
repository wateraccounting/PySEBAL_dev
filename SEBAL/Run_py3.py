# -*- coding: utf-8 -*-
"""
Created on 03 Dec 2019

@author: tih, sajid pareeth
"""

import pysebal_py3
import os
from openpyxl import load_workbook
##### USER INPUTS

##### For Linux SET THE PATH TO INPUT EXCEL SHEET #####
#inputExcel = r"/mnt/d/PySEBAL_dev/test_data/InputEXCEL_v3_3_7_LIN.xlsx"

current_wd = os.getcwd()
dir_back = os.getcwd() + "\\..\\"
os.chdir(dir_back)
pySEBAL_Base_dir = os.getcwd()

SEBAL_dir = pySEBAL_Base_dir + "\\SEBAL"
os.chdir(SEBAL_dir)

inputExcel = pySEBAL_Base_dir + "\\test_data\\InputEXCEL_v3_3_7_WIN.xlsx"
input_dir = pySEBAL_Base_dir + "\\test_data\\input\\insat"
output_dir = pySEBAL_Base_dir + "\\test_data\\output"
DEM_dir = pySEBAL_Base_dir + "\\test_data\\input\\dem_dal.tif"


workbook = load_workbook(filename=inputExcel)
sheet = workbook['General_Input']

sheet["B2"] = input_dir
sheet["C2"] = output_dir
sheet["E2"] = DEM_dir

workbook.save(filename = inputExcel)

st = 2 # starting row number
en = 2 # ending row number

####### USER INPUTS FINISH HERE

for number in range(st, en + 1):
    try:
        print ('starting line num: %d' % number)
        pysebal_py3.SEBALcode(number,inputExcel)
        print ('line num: %d done' % number)   
    except:
        print ('SEBAL did not run line %d fully' % number)
