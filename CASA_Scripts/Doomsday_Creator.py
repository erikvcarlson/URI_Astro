import csv

with open('/home/main/Downloads/Overly_Complete_Sample_Master_List.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

with open('/home/main/Downloads/Overly_Complete_Sample_SDSS.csv', newline='') as csvfile:
    data1 = list(csv.reader(csvfile))

for x in range(len(data1)):
    for y in range(len(data)):
        if data1[x][0] == data[y][0]:
            data[y][3] = data1[x][3] 

with open('The_Masterpiece.csv',mode='w') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',')
    for z in range(len(data)):
        csv_writer.writerow(data[z])

