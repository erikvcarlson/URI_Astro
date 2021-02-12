########
#Author: Erik Carlson
#Released Under Mozilla Public License 2.0
#Release Date: 12 Feb 2021
#Description: This script is to be used on a NRAO computing cluster on an interactive node. It is to copied and pasted
# into an interactive version of CASA. It utilizes two CSV files, one containing the right ascenstion and declination of the VLA phase
# calibrators and another containg the right ascestion and declination of the user's sources of interest.  The script takes a series of 
# ASDM files pulled off the NRAO cluster, converts them to measurement sets, splits off the users sources (including flux and phase calibrators) 
# and then performs the hanningsmooth function on the data. Future versions will enable to user to select specified bands for splitting. 
#######

#We start by importing the require python packages. These should be preinstalled on the NRAO computing cluster.

import csv
import re
from os import listdir
import shutil

#The user needs to replace this line with where they are keeping the preprocessed ASDM files. 
file_path = '/lustre/aoc/observers/nm-11325/Rest_of_Survey'

#The below code generates a list of files for the script to operate on. Make sure that you have removed all files that are not 
#ASDM files from the archive. 

list_of_files = os.listdir(file_path)
print('Files Compiled into a List')
validation_string = 'There is a total of ' + str(len(list_of_files)) +' files.'
print(validation_string)

#The below loop performs the following actions on each file: 
# 1) Reads in the files using importasdm 
# 2) Generates a list of the observations using the listobs comnmand 
# 3) Iterates through the text document to generate a list of flux and phase calibrators and sources 
# 4) Splits off the parallel hands ('RR,LL')  data using the split command
# 5) Performs the hanningsmooth command on the data 
# 6) Deletes the Orginal Measurement Set 


for a in range(len(list_of_files)):
    start_string = 'Working on File ' + str(a+1)
    print(start_string)
    asdm_name = list_of_files[a]
    vis_name = 'vis.ms'
    list_name = 'listobs.txt'
    importasdm(asdm = asdm_name, vis = vis_name)
    listobs(vis = vis_name, listfile = list_name, overwrite = True)
    output_string = 'File Number '  + str(a+1) +' is imported.'
    print(output_string)
    
    f_read = open("/lustre/aoc/observers/nm-11325/Rest_of_Survey/listobs.txt", "r")
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

    f_read.close()
    
    #The below section (that is commented out) is the precusor to using the regular expression package to help identify various bands 
    

    # f_read = open(file_path + "/listobs.txt", "r")
    # area_of_interest = f_read.readlines()[end_line:sources_line]
    
    # primary_spw = set()
    # secondary_spw = set()

    # for beta in range(len(area_of_interest)):
    #     p = str(area_of_interest[beta])
    #     p = p.split(' ')
    #     for z in range(len(p)):
    #         matchObj = re.search('^([1][0-9]+|[0~9]+|[0~9]*\.[0]+|[0]+|[0])', p[z])
    #         #print(matchObj)
    #         if matchObj:
    #             primary_spw.add(beta-2)
    #         else:
    #             pass

    #         matchObj_1 = re.search('^([456][0-9]+|[0~9]+|[0~9]*\.[0]+|[0]+|[0])', p[z])
    #         #print(matchObj)
    #         if matchObj_1:
    #             secondary_spw.add(beta-2)
    #         else:
    #             pass

    #f_read.close()    

    f_read = open("/lustre/aoc/observers/nm-11325/Rest_of_Survey/listobs.txt", "r")
    area_of_interest = f_read.readlines()[start_line:end_line]
    source_list = ''

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
        Flux_Calibrators = [[202.784541667,30.50915], [24.4220809625,33.1597591639], [80.2911917542,16.6394586722], [85.65057465,49.8520093222], [212.836032083,52.2025391667] ]

        for x  in range(len(Flux_Calibrators)):
            RA_Flux = Flux_Calibrators[x][0]
            Dec_Flux = Flux_Calibrators[x][1]
            if abs(RA_Flux - RA) < .1 and abs(Dec_Flux - Dec) < .1 :
                print('Flux Calibrator Found!')
                source_list = source_list + str(y) + ','
        
        #Find the Phase Calibrator 

        Phases = []
        with open('/lustre/aoc/observers/nm-11325/Files/All_Phase_Calibrators.csv') as csvfile:
            reader = csv.reader(csvfile, quoting = csv.QUOTE_NONNUMERIC)
            for row in reader:
                Phases.append(row)
        
        for x in range(len(Phases)):
            RA_Phase = Phases[x][0]
            Dec_Phase = Phases[x][1]
            if abs(RA_Phase - RA) < .1 and abs(Dec_Phase - Dec) < .1 :
                print('Phase Calibrator Found!')
                source_list = source_list + str(y) + ','


        #Find Targets 

        Sources = []

        with open('/lustre/aoc/observers/nm-11325/Files/source.csv') as csvfile:
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

    #This commented out section is the precusor for dealing with multibanded measurement sets where data is split 
    #by band instead of being handed to the user as a lump sum dataset. As you can see various parts of the code are 
    #duplicated and are commented out for the purposes of this release. 
    
    # spw_string = ''
    # spw1_string = ''
    # primary_spw = list(primary_spw)
    # secondary_spw = list(secondary_spw)

    print('Source List Compiled')
    
    # for c in range(len(primary_spw)):
    #     if primary_spw[c] == primary_spw[0]:
    #         spw_string = str(primary_spw[0])
    #     else:
    #         spw_string = spw_string + ',' + str(primary_spw[c])

    # for d in range(len(secondary_spw)):
    #     if secondary_spw[d] == secondary_spw[0]:
    #         spw1_string = str(secondary_spw[0])
    #     else:
    #         spw1_string = spw1_string + ',' + str(secondary_spw[d])

    try:         
        split(vis='vis.ms/',datacolumn='data',field=source_list,outputvis='split.ms',correlation='RR,LL')
        print('Sample Split Off Successfully')
        outputvis_string = str(a) + '.ms'
        hanningsmooth(vis='split.ms',outputvis = outputvis_string)
    except:
        pass

    #try:
        #split(vis='vis.ms/',datacolumn='data',field=source_list,outputvis='split1.ms',correlation='RR,LL',spw = '0.9~2.0GHz')
        #print('L-Band Sample Split Off Successfully')
        #outputvis_string = str(a) + 'L'+'.ms'
        #hanningsmooth(vis='split1.ms',outputvis = outputvis_string)
    #except:
        #pass


    try:
        shutil.rmtree('/lustre/aoc/observers/nm-11325/Rest_of_Survey/split.ms')
    except:
        pass
    #try:
        #shutil.rmtree('/lustre/aoc/observers/nm-11325/Rest_of_Survey/split1.ms')
    #except:
        #pass

    shutil.rmtree('/lustre/aoc/observers/nm-11325/Rest_of_Survey/vis.ms')
    shutil.rmtree('/lustre/aoc/observers/nm-11325/Rest_of_Survey/vis.ms.flagversions')
    remove_name = '/lustre/aoc/observers/nm-11325/Rest_of_Survey/' + asdm_name
    shutil.rmtree(remove_name)
    
    print('File Completed!')




