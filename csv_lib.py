import csv

def csv_fwrite(fname, fhead, fdata):
    if len(fname) == 0:
        fname = 'out.csv'
    f = open(fname, 'w', newline='', encoding="utf-8")
    writer = csv.writer(f, delimiter=",")
    
    if len(fhead) != 0:
        writer.writerow(fhead)
        
    for line in fdata:
        writer.writerow(row)
    f.close()
    
def csv_fread(fname)
    with open(fname) as csv_file:
        return csv.reader(csv_file, delimiter=',')


import pandas
def csv_fread_pd(fname)
    return pandas.read_csv(fname)

