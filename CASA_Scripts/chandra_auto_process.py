import os
import shutil

file_path = '/home/main/Research/Chandra_Data/Data_2/'
list_of_files = os.listdir(file_path)

os.system('ciao -o')

for a in range(len(list_of_files)):
    filename = list_of_files[a]
    pix = "pix_adj='edser' "
    chandra_command = 'chandra_repro ' + filename + ' ' +filename +'/repro ' + pix  
    os.system(chandra_command)
