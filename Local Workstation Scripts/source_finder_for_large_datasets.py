########
#Author: Erik Carlson
#Released Under Mozilla Public License 2.0
#Release Date: 12 Feb 2021
#Description: This script is to be used on a local worksation to aid in the reduction of EVLA or VLA data using CASA. 
# This script takes in a measurement set created by the split_automation_script and identifies flux and phase calibrators, 
# and sources for the user to add to their reduction script. The user must first define the name of the measurement defined
# in the variable myvis. Much like in the split_automation_script the user must point to their source.csv, and All_Phase_Calibrators.csv 
# files. 
#######

# We start my pointing at the required python packages we are using. To install please see the doucmentation for pip. 
import csv
import re
from os import listdir
import shutil

#The user must define the name of their measurement set either here or in CASA. Variables in CASA will translate to this script. 
vis_name = myvis
list_name = 'listobs.txt'
listobs(vis = vis_name, listfile = list_name, overwrite = True)
file_path = os.getcwd()
    
f_read = open(file_path + "/listobs.txt", "r")
tail_of_logger = f_read.readlines()
my_string = 'Fields: '
for x in range(len(tail_of_logger)):
    p = str(tail_of_logger[x]).find(my_string)
    if p != -1: 
        start_line = x+2
        break
my_string = 'Spectral Windows:'
for x in range(len(tail_of_logger)):
    p = str(tail_of_logger[x]).find(my_string)
    if p != -1: 
        end_line = x
        break
my_string = 'Sources:'
for x in range(len(tail_of_logger)):
    p = str(tail_of_logger[x]).find(my_string)
    if p != -1: 
        sources_line = x
        break
my_string = 'Antennas:'
for x in range(len(tail_of_logger)):
    p = str(tail_of_logger[x]).find(my_string)
    if p != -1: 
        ant_line = x
        break

f_read.close()
    
   
f_read = open(file_path + "/listobs.txt", "r")
area_of_interest = f_read.readlines()[start_line:end_line]
source_list = ''
phase_list = ''
flux_list =''
    
    
#The below loop colates the list of sources in the observation. 
    
for y in range(len(area_of_interest)):
    p = str(area_of_interest[y])
    p = p.split(' ')
    for z in range(len(p)):
        #print(p[z])
        #p[z] = '05:42:36.137916'
        matchObj = re.search('^([0-9][0-9](\:[0-9]\d){2}|90(\:00){5})', p[z])
        #print(matchObj)
        if matchObj:
            RA_user_input = p[z]
        else:
            pass
        matchObj = re.search('^[+-]([0-9][0-9](\.[0-9]\d){2}|90(\.00){5})', p[z]) 
        if matchObj:
            Dec_user_input = p[z][1:]
            
    hours = float(RA_user_input.split(':')[0])
    minutes = float(RA_user_input.split(':')[1])
    seconds= float(RA_user_input.split(':')[2])

    RA = ((hours + (minutes/60) + (seconds/3600))) *15
    Degrees = float(Dec_user_input.split('.')[0])
    minutes = float(Dec_user_input.split('.')[1])
    seconds= float(Dec_user_input.split('.')[2])

    Dec = (Degrees+ minutes/60 + seconds / 3600)

    current_source = [RA,Dec]
    #Find Flux Calibration 
    Flux_Calibrators = [[202.784541667,30.50915,'3C286'], [24.4220809625,33.1597591639, '3C48'], [80.2911917542,16.6394586722,'3C138'], [85.65057465,49.8520093222,'3C147'], [212.836032083,52.2025391667,'3C295'] ]

    for x  in range(len(Flux_Calibrators)):
        RA_Flux = Flux_Calibrators[x][0]
        Dec_Flux = Flux_Calibrators[x][1]
        if abs(RA_Flux - RA) < .1 and abs(Dec_Flux - Dec) < .1 and len(flux_list) < 1:
            print('Flux Calibrator Found!')
            flux_name = Flux_Calibrators[x][2]
            flux_list = flux_list + str(y) + ','
        
    #Find the Phase Calibrators. This is where the user needs to point to their phase calibrators file 

    Phases = []
    with open('/home/main/Research/CASA_Automation/All_Phase_Calibrators.csv') as csvfile:
        reader = csv.reader(csvfile, quoting = csv.QUOTE_NONNUMERIC)
        for row in reader:
            Phases.append(row)
        
    for x in range(len(Phases)):
        RA_Phase = Phases[x][0]
        Dec_Phase = Phases[x][1]
        if abs(RA_Phase - RA) < .1 and abs(Dec_Phase - Dec) < .1 :
            print('Phase Calibrator Found!')
            phase_list = phase_list + str(y) + ','

    #Find Targets. This is where the user needs to point to their source file.  

    Sources = []

    with open('/home/main/Research/CASA_Automation/sources.csv') as csvfile:
        reader = csv.reader(csvfile, quoting = csv.QUOTE_NONNUMERIC)
        for row in reader:
            Sources.append(row)

    for x in range(len(Sources)):
        RA_Source = Sources[x][0]
        Dec_Source = Sources[x][1]
        if abs(RA_Source - RA) < .1 and abs(Dec_Source - Dec) < .1 :
            print('Source Found!') 
            source_list = source_list + str(y) + ','


source_list = source_list[0:-1]
phase_list = phase_list[0:-1]
flux_list = flux_list[0:-1]
    
    
f_read.close()

# The below section is to generate a list of sources that are not phase calibrators to determine if the full roberts script is needed. 
#This piece of code does not work as of this release. 

#test_str1 = source_list
#test_str2 = phase_list
#res = "" 
#for i in test_str1: 
#    if i in test_str2 and not i in res: 
#        res += i 
#        
#source_phase_intersect = res
 
print('Source List Compiled')

