import csv
import re
from os import listdir
import shutil

file_path = '/lustre/aoc/observers/nm-11325/Rest_of_Survey'

list_of_files = os.listdir(file_path)
print('Files Compiled into a List')
validation_string = 'There is a total of ' + str(len(list_of_files)) +' files.'
print(validation_string)
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

    f_read.close()

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
    
    print('Source List Compiled')
    
    split(vis='vis.ms/',datacolumn='data',field=source_list,outputvis='split.ms')
    
    print('Source Sample Split Off Successfully')
    
    outputvis_string = str(a) + '.ms'
    hanningsmooth(vis='split.ms',outputvis = outputvis_string)
    shutil.rmtree('/lustre/aoc/observers/nm-11325/Rest_of_Survey/split.ms')
    shutil.rmtree('/lustre/aoc/observers/nm-11325/Rest_of_Survey/vis.ms')
    shutil.rmtree('/lustre/aoc/observers/nm-11325/Rest_of_Survey/vis.ms.flagversions')
    remove_name = '/lustre/aoc/observers/nm-11325/Rest_of_Survey/' + asdm_name
    shutil.rmtree(remove_name)
    
    print('File Completed!')





