#Author: Erik Carlson 
#Description: This Script takes a user provided Right Ascention and Declination as defined on lines 16 and 17 and provides the user with the measurement set identification of the quicklook images
#This script requires the use of Python 3 to run properly 
#Future Changes: Provide the User with Multi-Epoch datasets. Expand to fields that are on the edges of tiles
import urllib
import urllib.request
import re
import pandas

url = "https://archive-new.nrao.edu/vlass/quicklook/listing.txt"
file = urllib.request.urlopen(url)

#intake and validate values from the user
a = 0
while a ==0: 
    try: 
        RA = input("Please Enter your Right Ascention in Decimal Format: ") #121.98974
        DEC = input("Please Enter your Right Ascention in Decimal Format: ") #4.54293
        Epoch = input("Please Enter the Requested Epoch (1/2), leave blank if unknown: ")
        RA = float(RA)
        DEC = float(DEC)
        if Epoch == '':
            Epoch = '1'
        Epoch = int(Epoch)
        break
    except: 
        print("Incorrect Values Entered")

df = pd.read_csv("Tiles_NoHead.tsv",sep='\t')
df.head()
"""
for line in file:
    decoded_line = line.decode("utf-8")
    try:
        #search for the J-name in each file name 
        m = re.search('J\d\d\d\d\d\d[+]\d\d\d\d\d\d', decoded_line)
        #convert that J name is RA and DEC is decimal format
        J2000  = m.group(0).replace('J','')
        RA_Hours = J2000[0:2]
        RA_Mins = J2000[2:4]
        Dec_Deg = J2000[7:9]
        Dec_Mins = J2000[9:11]
        RA_Degrees = float(RA_Hours)*15 + float(RA_Mins)/60
        Dec_Deg = float(Dec_Deg) + float(Dec_Mins)/60
        
        #search for an image within 2 radial degrees from the source in question
        if abs(RA - RA_Degrees) <= 2 and  abs(DEC - Dec_Deg) <= 2:
            tile_id = re.search('T\d\dt\d\d', decoded_line).group(0)
            VLASS_id_Regex = 'VLASS[' + str(Epoch) + '].\d' 
            VLASS_id = re.search(VLASS_id_Regex, decoded_line).group(0) 
            
            #Warning User of use of VLASS1.1 Data 
            if VLASS_id ==  'VLASS1.1':
                print('Using VLASS1.1 Data, proceed with caution. See VLASS Memo 13 for more Information')
            
            VLASS_Regex = VLASS_id.replace('.','[.]')
            full_regex = VLASS_Regex + '[.]ql[.]' + tile_id + '[.]J\d\d\d\d\d\d[+]\d\d\d\d\d\d[.]\d\d[.]\d\d\d\d[.]\S\S\S'
            file_to_search = re.search(full_regex,decoded_line).group(0)
            archive_search_file = "https://archive-new.nrao.edu/vlass/quicklook/" + VLASS_id + '/' + tile_id + '/' + file_to_search + 'casa_pipescript.py'
            break
    except:
        pass

try:
    url = archive_search_file
    search_file_for_ms =  urllib.request.urlopen(url)
    for line in search_file_for_ms:
        decoded_line = line.decode("utf-8")
        if decoded_line.find(str(VLASS_id)) != -1:
            start_value = int(decoded_line.find(str(VLASS_id)))
            print
            end_value = int(decoded_line.find('.ms'))
            measurement_set_name = decoded_line[start_value:end_value]
            print(measurement_set_name)
except:
    print('Error Occured. It is possible there is no VLASS dataset for the data in question.')
"""
