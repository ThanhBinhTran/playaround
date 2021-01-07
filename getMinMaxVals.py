#!/usr/bin/python
import StringIO
import csv
import array

arrayMin = []
arrayMax = []
header   = []
line_num = 0
maxminfile = "MinMaxValues.csv"
infile = 'all.csv'
target = open(maxminfile, 'w')

print("querying MAX MIN values\n")

with open(infile, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			line_num = line_num + 1
			if line_num == 1:
				for index in range(len(row)):
					header.insert(index, row[index])
			if line_num == 2:
				for index in range(len(row)):
					arrayMax.insert(index, row[index])
					arrayMin.insert(index, row[index])
			elif line_num > 2:
				for index in range(len(row)):
					if float(arrayMax[index]) < float(row[index]):
						arrayMax[index] = row[index]
					if float(arrayMin[index]) > float(row[index]):
						arrayMin[index] = row[index]
			#print ("ARR" ,row)
			#print ("MAX" ,arrayMax)
			#print ("MIN",arrayMin)
			#print (line_num)
			
# write to file [header, maximum value, minimum vale]
target.write("Features, Maximum Value, Minimum Value\n")
for index in range(len(header)):
	target.write(header[index] +',' + arrayMax[index] + ',' +  arrayMin[index] )
	target.write('\n')

print("DONE\n")
print("open " + maxminfile  + " to get max,min values")
