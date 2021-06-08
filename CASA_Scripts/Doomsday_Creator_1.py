import csv

with open('/home/main/Research/CASA_Scripts/The_Masterpiece.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

with open('/home/main/Research/CASA_Scripts/NED_Results.csv', newline='') as csvfile:
    data1 = list(csv.reader(csvfile))
with open('/home/main/Downloads/Completion.csv', newline='') as csvfile:
    data2 = list(csv.reader(csvfile))


for x in range(len(data1)):
    for y in range(len(data)):
        if abs(float(data1[x][1]) - float(data[y][1])) < 0.0084 and abs(float(data1[x][2]) - float(data[y][2])) < 0.0084: #30 arcsecond search
            data[y][3] = data1[x][0] #sets the name
            data[y][5] = data1[x][3] #sets the type
            if data[y][4] == '':
                data[y][4] = data1[x][4] #inputs empty redshifts
final_list = []

for m in range(len(data2)):
    for o in range(len(data)):
        if abs(float(data2[m][2]) - float(data[o][2])) < 0.0084 and abs(float(data2[m][3]) - float(data[o][2])) < 0.0084:
            data[o][4] = data2[m][6]

for l in range(len(data)):
    if data[l][3] == '':
        data[l][3] = data[l][0]
    if data[l][4] == '':
        data[l] = ['','','','','','','']



for n in range(len(data)):
    if data[n] == ['','','','','','',''] or float(data[n][4]) > 2.5: 
        pass
    elif float(data[n][4]) < 2.4 and float(data[n][6]) < 77.36:
        data[n] = []
    elif float(data[n][4]) < 2.3 and float(data[n][6]) < 85.87:
        data[n] = []
    elif float(data[n][4]) < 2.2 and float(data[n][6]) < 95.78:
        data[n] = []
    elif float(data[n][4]) < 2.1 and float(data[n][6]) < 107.41:
        data[n] = []
    elif float(data[n][4]) < 2.0 and float(data[n][6]) < 121.15:
        data[n] = []
    elif float(data[n][4]) < 1.9 and float(data[n][6]) < 137.53:
        data[n] = []
    elif float(data[n][4]) < 1.8 and float(data[n][6]) < 157.25:
        data[n] = []
    elif float(data[n][4]) < 1.7 and float(data[n][6]) < 181.21:
        data[n] = []
    elif float(data[n][4]) < 1.6 and float(data[n][6]) < 210.71:
        data[n] = []
    elif float(data[n][4]) < 1.5 and float(data[n][6]) < 247.45:
        data[n] = []
    elif float(data[n][4]) < 1.4 and float(data[n][6]) < 293.91:
        data[n] = []
    elif float(data[n][4]) < 1.3 and float(data[n][6]) < 353.67:
        data[n] = []
    elif float(data[n][4]) < 1.2 and float(data[n][6]) < 432:
        data[n] = []
    elif float(data[n][4]) < 1.1 and float(data[n][6]) < 536.95:
        data[n] = []
    elif float(data[n][4]) < 1.0 and float(data[n][6]) < 681.38:
        data[n] = []
    elif float(data[n][4]) < 0.9 and float(data[n][6]) < 886.24:
        data[n] = []
    elif float(data[n][4]) < 0.8 and float(data[n][6]) < 1187.87:
        data[n] = []
    elif float(data[n][4]) < 0.7 and float(data[n][6]) < 1653.31:
        data[n] = []
    elif float(data[n][4]) < 0.6 and float(data[n][6]) < 2415.21:
        data[n] = []
    elif float(data[n][4]) < 0.5 and float(data[n][6]) < 3764.26:
        data[n] = []
    elif float(data[n][4]) < 0.4 and float(data[n][6]) < 6427.76:
        data[n] = []
    elif float(data[n][4]) < 0.3 and float(data[n][6]) < 12629.23:
        data[n] = []
    elif float(data[n][4]) < 0.2 and float(data[n][6]) < 31827.32:
        data[n] = []
    elif float(data[n][4]) < 0.1 and float(data[n][6]) < 145057.29:
        data[n] = []



   
final_list = data
with open('The_Revised_Masterpiece.csv',mode='w') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',')
    for z in range(len(final_list)):
        csv_writer.writerow(final_list[z])

