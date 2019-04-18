import csv
import os
from skimage.io import imread, imshow
import matplotlib.pyplot as plt
annotations_path = "Annotations/annotations_trimmed.csv"
inputFile = open(annotations_path, "r", newline='')

reader = csv.reader(inputFile)
next(reader)
entry = next(reader)
nonEmpty = True
while nonEmpty:
	alias = entry[0]
	image = imread(alias)
	print("Working with image:" + alias.strip("Images/blouse/"))
	print("y: " + str(len(image)) + "\nx: " + str(len(image[0])))
	# imshow(image)
	# plt.show()
	# alias = alias.split("/")
	# if alias[1] == "blouse" and alias[2] in ids:
	# 	writer.writerow(entry)
	localAreas = []
	for landmark in entry[2:]:
		coordinates = landmark.split('_')
		for i in range(len(coordinates)):
			print(coordinates[i])
			coordinates[i] = int(coordinates[i])
		if coordinates[0] != -1:
			section = image[max(coordinates[1] - 20, 0): min(coordinates[1] + 20,len(image)),
			max(coordinates[0] - 20, 0): min(coordinates[0] + 20,len(image[0])) ]
			
	try:
		entry = next(reader)
	except Exception as e:
		nonEmpty = False

inputFile.close()

