from scipy.spatial.distance import cosine
import csv
import cv2
import numpy as np








def execute(input_path = "testSpread.csv", output_path = "results.csv", database_path = 'Landmark_BRIEF_features.csv',
			image_base_path = 'Data/blouseData/', keypoint_size = 64.0, landmark_constant = 1.0, feature_coefficient = 0.0025):
	inputFile = open(input_path, "r", newline='')
	outputFile = open(output_path, "w", newline='')
	writer = csv.writer(outputFile)
	reader = csv.reader(inputFile)
	brief = cv2.xfeatures2d.BriefDescriptorExtractor_create(bytes=32)

	next(reader)
	line = next(reader)

	subject = []
	subject.append(line[0])
	landmarks = []
	for coordinates in line[2:]:
		landmarks.append(coordinates.split("_")[:2])
	for coordinates in landmarks:
		for i in range(len(coordinates)):
			coordinates[i] = float(coordinates[i])
	subject.append(landmarks)
	features = []
	for coordinates in landmarks:
		if coordinates[0] != -1:
			features.append(cv2.KeyPoint(x=coordinates[0], y=coordinates[1], _size=keypoint_size))

	image = cv2.imread(image_base_path + subject[0], 3)
	kp, des = brief.compute(image, features)
	subject.append(des)

	inputFile.close()
	inputFile = open(database_path, "r", newline='')

	reader = csv.reader(inputFile)
	next(reader)
	line = next(reader)
	l = 0
	nonEmpty = True
	results = [];
	while nonEmpty:
		print(line[0])
		comparison = []
		image = cv2.imread(image_base_path + line[0], 3)
		comparison.append(line[0])
		line[1] = line[1][1:-1]
		line[1] = line[1].split("],")
		for i in range(len(line[1])):
			line[1][i] = line[1][i].replace('[', '')
			line[1][i] = line[1][i].replace(']', '')
			line[1][i] = line[1][i].split(', ')
			line[1][i] = [float(line[1][i][0]), float(line[1][i][1])]
		# sys.exit()
		comparison.append(line[1])

		landmark_cosines = []

		for i in range(len(subject[1])):
			landmark_cosines.append(cosine(subject[1][i], comparison[1][i]))
		landmark_similarity = np.linalg.norm(landmark_cosines, ord=1)
		line[2] = line[2][1:-1]
		line[2] = line[2].split("]\n")
		for i in range(len(line[2])):
			line[2][i] = line[2][i].replace('[', '')
			line[2][i] = line[2][i].replace(']', '')
			line[2][i] = line[2][i].replace('\n', '')
			# print(line[2][i])
			line[2][i] = line[2][i].replace('  ', ' ')
			line[2][i] = line[2][i].replace('  ', ' ')

			line[2][i] = line[2][i][1:]
			line[2][i] = line[2][i].split(' ')

			descriptions = []
			try:
				for entry in line[2][i]:
					descriptions.append(float(entry))
			except ValueError:
				print(line[2])
				print(line[2][i])
			line[2][i] = descriptions

		comparison.append(line[2])
		feature_cosines = []
		# print(line[2][0])
		# sys.exit()
		subject_index = 0
		comparison_index = 0

		for i in range(len(subject[2])):
			if subject[1][i][0] != -1 and comparison[1][i][0] != -1:
				try:

					feature_cosines.append(cosine(subject[2][subject_index], comparison[2][comparison_index]))
				except ValueError:
					pass
			elif subject[2][i][0] == -1 and comparison[2][i][0] == -1:
				pass
			elif subject[2][i][0] == -1:
				comparison_index += 1
			else:
				subject_index += 1

		feature_similarity = np.linalg.norm(feature_cosines, ord=1)
		overall_similarity = (landmark_similarity * landmark_constant) + (feature_coefficient * feature_similarity)
		results.append([line[0], overall_similarity])

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

if __name__ == "__main__":
	execute()