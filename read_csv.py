import csv
with open('data.txt', 'rb') as csvfile:
   spamreader = csv.reader(csvfile, delimiter=',')
   for row in spamreader:
        print '___'.join(row)
