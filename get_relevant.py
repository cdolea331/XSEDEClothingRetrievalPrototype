import csv
import os
inputFile = open("Annotations/annotations.csv", "r", newline='')
outputfile = open("Annotations/annotations_trimmed.csv", "w", newline='')

reader = csv.reader(inputFile)
writer = csv.writer(outputfile)
ids = next(os.walk("Images/blouse"))[2]
next(reader)
entry = next(reader)
nonEmpty = True
while nonEmpty:
	alias = entry[0]
	print(alias)
	alias = alias.split("/")
	if alias[1] == "blouse" and alias[2] in ids:
		writer.writerow(entry)
	try:
		entry = next(reader)
	except Exception as e:
		nonEmpty = False

inputFile.close()
outputfile.close()
