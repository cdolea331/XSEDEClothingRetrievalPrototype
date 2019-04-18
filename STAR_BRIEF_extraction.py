import csv
import os
import sys
from math import sqrt
from math import pi
import cv2
import matplotlib.pyplot as plt
import time
image_base_path =  'Data/blouseData/'
annotations_path = 'Data/blouseData/annotations.csv'
output_path = "STAR_BRIEF_features.csv"
inputFile = open(annotations_path, "r", newline='')
outputFile = open(output_path, "w", newline='')
writer = csv.writer(outputFile)

print(cv2.__version__)



reader = csv.reader(inputFile)
next(reader)
entry = next(reader)
nonEmpty = True
imageData = []
imageNames = []
brief = cv2.xfeatures2d.BriefDescriptorExtractor_create(bytes=32)
star = cv2.xfeatures2d.StarDetector_create()
print(dir(cv2.ORB_create()))
# sys.exit()
l = 0
while nonEmpty:
	l += 1
	features = []
	alias = entry[0]
	image = cv2.imread(image_base_path + alias, 3)
	shift_index = 0
	kp = star.detect(image, None)
	kp, des = brief.compute(image, kp)
	imageData.append(des)
	imageNames.append(alias)
	try:
		entry = next(reader)
	except Exception as e:
		nonEmpty = False
i = 0
for data in imageData:
	outputFile.write(imageNames[i] + ",")
	execute = False
	try:
		len(data)
		execute = True
	except TypeError:
		pass
	if execute:
		for entry in data:

			outputFile.write(str(entry).replace("\n", ''))
			outputFile.write(",")
	i += 1
	outputFile.write("\n")

inputFile.close()
outputFile.close()


