from scipy.spatial.distance import cosine
import csv
import os
from math import sqrt
from math import pi
import cv2
from Data.helperFunctions import rectifyZeroVector
# from skimage.io import imread, imshow
import matplotlib.pyplot as plt
import numpy as np
import sys
extractor = "SIFT"
descriptor = "BRIEF"
argument_path = extractor + "_" + descriptor + "_input.csv"
image_base_path = 'Data/toyDataSet/'
annotations_path = extractor + '_' + descriptor + '_features.csv'
output_path = extractor + "_" + descriptor + "_results.csv"
landmark_constant = 0.0
feature_coefficient = 0.0025
np.seterr(all='raise')
inputFile = open(argument_path, "r", newline='')
outputFile = open(output_path, "w", newline='')
writer = csv.writer(outputFile)
reader = csv.reader(inputFile)
descriptor = cv2.xfeatures2d.BriefDescriptorExtractor_create(bytes=32)
if descriptor == "ORB":
    descriptor = cv2.ORB_create()

line = next(reader)
inputVectors = (line[1:])

for i in range(len(inputVectors)):
	inputVectors[i] = inputVectors[i][2:-1].split(" ") #.split(" ").replace(" ", "")
	while '' in inputVectors[i]:
		inputVectors[i].remove('')
	for j in range(len(inputVectors[i])):
		inputVectors[i][j] = int(inputVectors[i][j])
while [] in inputVectors:
    inputVectors.remove([])
# sys.exit()

inputFile.close()
inputFile = open(annotations_path, "r", newline='')

reader = csv.reader(inputFile)
next(reader)
line = next(reader)
l = 0
nonEmpty = True
results = []
while nonEmpty : #and line[0][7] == "b"
    print(line[0])
    comparisonVectors = (line[1:])

    for i in range(len(comparisonVectors)):
        # print(comparisonVectors[i])
        comparisonVectors[i] = comparisonVectors[i][1:-1].split(" ")  # .split(" ").replace(" ", "")
        while '' in comparisonVectors[i]:
            comparisonVectors[i].remove('')
        for j in range(len(comparisonVectors[i])):
            comparisonVectors[i][j] = int(comparisonVectors[i][j])
    while [] in comparisonVectors:
        comparisonVectors.remove([])

    shortVector = comparisonVectors if len(comparisonVectors) < len(inputVectors) else inputVectors
    longVector = inputVectors if len(comparisonVectors) < len(inputVectors) else comparisonVectors
    while len(shortVector) < len(longVector):
        padVector = []
        for i in range(32):
            padVector.append(-1)
        shortVector.append(padVector)
    similarity = []
    for i in range(len(shortVector)):
        shortVector[i] = rectifyZeroVector(shortVector[i])
        longVector[i] = rectifyZeroVector(longVector[i])
        if(i < len(shortVector) - 1):
            try:
                similarity.append(cosine(shortVector[i], longVector[i]))
            except RuntimeError:
                print(comparisonVectors[i],"\n", inputVectors[i])
                print(len(comparisonVectors[i]), "\n", len(inputVectors[i]))
                print(shortVector[i],"\n", longVector[i])


    similarity = np.linalg.norm(similarity, ord=1)

    results.append([line[0], similarity])

    l += 1
    try:
        line = next(reader)
    except Exception as e:
        nonEmpty = False
for i in range(len(results)):
    if np.isnan(results[i][1]):
        results[i][1] = -1

results = sorted(results, key=lambda t: t[1])

for entry in results:
    writer.writerow(entry)

inputFile.close()
outputFile.close()
