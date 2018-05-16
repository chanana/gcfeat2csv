import sqlite3
import csv
from os import listdir
import re

mypath = "./gcfeat/"
result_file = "Features.csv"
onlyfiles = [mypath+f for f in listdir(mypath) if f != ".DS_Store"]
pattern = re.compile("\d+-\d+")
filenames = []

for f in onlyfiles:
    # Get sample name (XX-XX)
    filename = re.search(pattern=pattern, string=f)
    if filename.group(0) in filenames:
        print("Duplicate File! Skipping {}".format(filename.group(0)))
        continue
    else:
        filenames.append(filename.group(0))
        print(filename.group(0))
    
    # open connection to database file; select columns
    conn = sqlite3.connect(f)
    c = conn.cursor()
    c.execute('SELECT mz, apex_intensity, apex_rt FROM features')
    
    with open(result_file, 'a') as f:
        fwriter = csv.writer(f, delimiter=',')
        
        # get data
        data = c.fetchall()
        
        # add sample name to a row
        for tuple_row in data:
            # mz_rt = 'mz'_'apex_rt'
            # mz and apex_rt rounded to 4 decimal places
            # mz_rt = str(round(tuple_row[0], 4)) + "_" + str(round(tuple_row[2], 4)) # make mz_rt pair
            
            # ['xx-xx', mz, rt, apex_intensity]
            row = [filename.group(0), round(tuple_row[0],4), round(tuple_row[2],2), round(tuple_row[1],4)]
            
            # write this row to the csv file
            fwriter.writerow(row)
    conn.close()
print("Done")

