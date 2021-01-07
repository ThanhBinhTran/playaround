#!/usr/bin/python
import StringIO
import csv
import math

line_num  = 0
firstLine = 1   # true
index     = 0
lData = []  # data in line 
header = [] # header (index, content)

MaxArray = []
MinArray = []
maxminfile = "MinMaxValues.csv"
outfile  = "allCoverted.csv"
infile   = 'all.csv'

target = open(outfile, 'w')

print ("Converting values")
# get maximum, minimum values of features
# run "python getMinMaxVal.py" to create MinMaxValue.csv

with open(maxminfile, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			line_num  = line_num + 1
			if line_num > 1:
				MaxArray.insert(index, row[1])
				MinArray.insert(index, row[2])
				index = index + 1
				
#print ("MAXvalues", MaxArray)
#print ("MINvalues", MinArray)
				
with open(infile, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			if firstLine == 1:
				firstLine = 0
				for idx in range(len(row)):
					lData.insert(idx, row[idx])
					header.insert(idx, row[idx])
				#print ("Header line")
			else:
				#print ("data lines")
				for idx in range(len(row)):
					if header[idx] == "totalSourceBytes"  or \
						header[idx] == "totalDestinationBytes" or \
						header[idx] == "totalDestinationPackets" or \
						header[idx] == "totalSourcePackets":
						lData[idx] = str(math.log10(float(row[idx]) - float(MinArray[idx]) + 1))
					elif header[idx] == "source"  or \
						header[idx] == "destination" or \
						header[idx] == "destinationPort" or \
						header[idx] == "startDateTime":
						lData[idx] = str( (float(row[idx]) - float(MinArray[idx]))/( float(MaxArray[idx]) + float(MinArray[idx])))
					else:
						lData[idx] = row[idx]
						
			target.write(','.join(lData) )
			target.write('\n')
			#print("--------------------------------")
			#print(lData)
print("DONE")

