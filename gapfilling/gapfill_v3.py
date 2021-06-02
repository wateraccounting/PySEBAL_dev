# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Sajid Pareeth, 2020
The script does post processing of PySEBAL outputs.
averaging, mm/day to mm/month, gap filling using gap filling
'''

import os
import subprocess
import sys

## Set Environment variables
os.environ['GRASSBIN'] = 'C:\\OSGeo4W64\\bin\\grass78'
os.environ['GISRC'] = 'C:\\OSGeo4W64\\apps\\grass\\grass78\\demolocation\\.grassrc78'
test = os.getenv('GISRC')
print(test)
#os.environ['path'] += os.pathsep + os.pathsep.join(['C:\\OSGeo4W64\\apps\\grass\\grass78\\lib']) + os.pathsep.join(['C:\\OSGeo4W64\\apps\\grass\\grass78\\bin']) + os.pathsep.join(['C:\\OSGeo4W64\\apps\\grass\\grass78\\scripts'])
sys.path.append('C:\\OSGeo4W64\\apps\\grass\\grass78\\lib')
sys.path.append('C:\\OSGeo4W64\\apps\\grass\\grass78\\bin')
sys.path.append('C:\\OSGeo4W64\\apps\\grass\\grass78\\scripts')
print(sys.path)
import shutil
import glob
import grass_session
from grass_session import Session
import grass.script as grass
import pdb
import datetime
import pandas as pd
from calendar import monthrange


#set GRASSBIN=C:\OSGeo4W64\bin\grass78
#set GISRC=C:\OSGeo4W64\apps\grass\grass78\demolocation\.grassrc78
#set PATH=%PATH%;C:\OSGeo4W64\apps\grass\grass78\lib;C:\OSGeo4W64\apps\grass\grass78\bin;C:\OSGeo4W64\apps\grass\grass78\scripts
###

## r.series.lwr -l -h -i input=$maps suffix=_lwr order=2 weight=tricube range=0,inf fet=0.5 dod=3 maxgap=3 --o
## r.hants -l -h -i input=$maps suffix=_hants range=0,inf nf=3 fet=0.5 --o 

## USER INPUTS ##
W=589983.538 #(minX)
S=3589887.628 #(minY)
E=651032.226 #(maxX)
N=3608130.224# (maxY)
res=30 # Spatial resolution of the input maps
INDAT="G:\IHE_Projects\Iran_Roodasht\SEBAL_ETa\input" # Input directory where all the PySEBAL outputs are stored, Eg: All ETa maps in one folder - THIS FOLDER SHOULD NOT HAVE ANY OTHER FILES
OUTDAT="G:\IHE_Projects\Iran_Roodasht\SEBAL_ETa\output" # Empty output folder where the gap-filled files will be stored
CRS='EPSG:32639' # CRS of the input maps. Output maps will be in the same CRS
gisdb='D:\\grasstemp' # A temporary folder (Empty) to process the files.
ST='2014_01' # START year and month
EN='2019_04' # End year and month
VAR="ETa" # The variable to post process. "ETa" for Actual EvapoTranspiration, "BIO" for Biomass Production, "ST" for surface temperature; "NDVI" for ndvi maps
##USER INPUTS FINISH HERE ###

START=datetime.datetime.strptime(ST, "%Y_%m")
END=datetime.datetime.strptime(EN, "%Y_%m")
months = [i.strftime("%Y_%m") for i in pd.date_range(start=START, end=END, freq='MS')]
#print(months)
locpth=gisdb + "\\TMPLOC"
if os.path.exists(locpth) and os.path.isdir(locpth):
    shutil.rmtree(locpth)


# set some common environmental variables, like:
os.environ.update(dict(GRASS_COMPRESS_NULLS='1',
                       GRASS_COMPRESSOR='ZSTD'))

# create a PERMANENT mapset
# create a Session instance
PERMANENT = Session()
PERMANENT.open(gisdb=gisdb, location='TMPLOC',
               create_opts=CRS)

# execute some command inside PERMANENT
#grass.run_command("g.mapsets",flags="l")
#grass.run_command("g.list", flags="m", type="rast")
# exit from PERMANENT
PERMANENT.close()

# create a new mapset in the same location
user = Session()
user.open(gisdb=gisdb, location='TMPLOC', mapset='TMPMAP',
               create_opts='')

# using grass.script
grass.run_command("g.extension", extension='r.series.lwr')
#grass.run_command("g.extension", extension='r.hants')
#grass.run_command("g.mapsets",flags="l")
grass.run_command("g.region", n=N, s=S, e=E, w=W, res=res, flags=["a"])
#grass.run_command("g.list", flags="f", type="rast")
s1="\\*.tif"
pt1=INDAT + s1
list=glob.glob(pt1)
for dt in list:
    out1=dt.rsplit('\\',1)[1]
    out2=out1.rsplit('.',1)[0]
    t=out1[::-1][11:18][::-1]
    dates=OUTDAT + "\\dates.txt"
    dates1=open(dates, "a+")
    dates1.write(t)
    dates1.write("\n")
    dates1.close()
    grass.run_command("r.in.gdal", input=dt, output=out2, overwrite=True)
    maps=OUTDAT + "\\maps.txt"
    grass.run_command("g.list", flags="m", type="rast", output=maps, overwrite=True)

## Remove Duplicate lines from dates.txt
dates2=OUTDAT + "\\dates_NW.txt"
lines_seen = set() # holds lines already seen
with open(dates2, "w") as output_file:
	for each_line in open(dates, "r"):
	    if each_line not in lines_seen: # check if line is not duplicate
	        output_file.write(each_line)
	        lines_seen.add(each_line)

for t in months:
    #print(t)
    tmp=OUTDAT + "\\tmp.txt"
    grass.run_command("g.list", flags="m", type="rast", pattern=f'*{t}*', output=tmp, overwrite=True)
    if os.stat(tmp).st_size == 0:
        grass.run_command("r.mapcalc", expression=f'map_avg_{t}_month = null()', overwrite=True)
    elif VAR == "NDVI":
        grass.run_command("r.series", file=tmp, output=f'map_avg_{t}_month', method='maximum', overwrite=True)
    else:
        grass.run_command("r.series", file=tmp, output=f'map_avg_{t}', method='average', overwrite=True)
        y=t[0:4]
        m=t[5:7]
        days=monthrange(int(y), int(m))[1]
        #print(days)
        grass.run_command("r.mapcalc", expression=f'map_avg_{t}_month = map_avg_{t} * {days}', overwrite=True)

maps1=OUTDAT + "\\maps_lwr.txt"
grass.run_command("g.list", type="rast", pattern='*_month$', output=maps1, overwrite=True)
grass.run_command("r.series.lwr", flags="lh", file=maps1, suffix='_lwr', order=0, weight='tricube', fet=0.5, dod=2, maxgap=3, overwrite=True)

for i in months:
    #print(i)
    grass.run_command("r.patch", input=f'map_avg_{i}_month,map_avg_{i}_month_lwr', output=f'map_avg_{i}_month_lwr_patch', overwrite=True)
    grass.run_command("r.fillnulls", input=f'map_avg_{i}_month_lwr_patch', output=f'map_avg_{i}_month_lwr_patch_fillnull', method='bilinear', npmin=600, segmax=300)
    grass.mapcalc('{r} = if({a} < 0, 0, {a})'.format(r=f'map_avg_{i}_month_lwr_patch_fillnull1', a=f'map_avg_{i}_month_lwr_patch_fillnull'))
    stats = grass.parse_command('r.univar', map=f'map_avg_{i}_month_lwr_patch_fillnull1', flags='eg', percentile='5,99')
    p2 = float(stats['percentile_5'])
    #print(p2)
    p99 = float(stats['percentile_99'])
    #print(p99)
    grass.mapcalc('{r} = if({a} < {lo}, {lo}, {a})'.format(r=f'map_avg_{i}_month_lwr_patch_fillnull2', a=f'map_avg_{i}_month_lwr_patch_fillnull1', lo=p2))
    grass.mapcalc('{r} = if({a} > {hi}, {hi}, {a})'.format(r=f'{VAR}_{i}_month_gapfilled', a=f'map_avg_{i}_month_lwr_patch_fillnull2', hi=p99))

grass.run_command("g.list", flags="m", type="rast")
maps_out=OUTDAT + "\\maps_out.txt"
grass.run_command("g.list", type="rast", pattern='*_gapfilled$', output=maps_out, overwrite=True)

with open(maps_out) as f:
  for dt1 in f:
        in1=dt1.strip('\n')
        out1=OUTDAT + "\\" + dt1.strip('\n') + ".tif"
        grass.run_command("r.out.gdal", input=in1, output=out1, overwrite=True)

files_text = os.listdir(OUTDAT)
for item in files_text:
    if item.endswith(".txt"):
        os.remove(os.path.join(OUTDAT, item))

user.close()
