import csv
from math import sqrt
import cv2





def execute(image_base_path='Data/blouseData/', annotations_path='Data/blouseData/annotations.csv',output_path="Landmark_BRIEF_features.csv",
			keypoint_size=64.0, use_threshold=True, threshold=5000):
	shift_size = (keypoint_size / 2) - 1
	diagonal_shift = (shift_size / sqrt(2)) // 1
	# Shift the keypoint of area by y and x values [area, y, x]
	landmark_shifts = [["neckline_left", shift_size, 0], ['neckline_right', shift_size, 0],
					   ['center_front', shift_size, 0], ['shoulder_left', diagonal_shift, diagonal_shift],
					   ['shoulder_right', diagonal_shift, -diagonal_shift],
					   ['armpit_left', -diagonal_shift, diagonal_shift],
					   ['armpit_right', -diagonal_shift, -diagonal_shift],
					   ['waistline_left', 0, shift_size], ['waistline_right', 0, -shift_size],
					   ['cuff_left_in', -diagonal_shift, -diagonal_shift],
					   ['cuff_left_out', -diagonal_shift, diagonal_shift],
					   ['cuff_right_in', -diagonal_shift, diagonal_shift],
					   ['cuff_right_out', -diagonal_shift, -diagonal_shift],
					   ['top_hem_left', -diagonal_shift, diagonal_shift],
					   ['top_hem_right', -diagonal_shift, -diagonal_shift],
					   ['waistband_left', diagonal_shift, diagonal_shift],
					   ['waistband_right', diagonal_shift, -diagonal_shift],
					   ['hemline_left', diagonal_shift, diagonal_shift],
					   ['hemline_right', diagonal_shift, -diagonal_shift], ['crotch', -shift_size, 0],
					   ['bottom_left_in', -diagonal_shift, -diagonal_shift],
					   ['bottom_left_out', -diagonal_shift, diagonal_shift],
					   ['bottom_right_in', -diagonal_shift, diagonal_shift],
					   ['bottom_right_out', -diagonal_shift, -diagonal_shift]]
	inputFile = open(annotations_path, "r", newline='')
	outputFile = open(output_path, "w", newline='')
	writer = csv.writer(outputFile)



	reader = csv.reader(inputFile)
	next(reader)
	entry = next(reader)
	nonEmpty = True
	imageData = []
	brief = cv2.xfeatures2d.BriefDescriptorExtractor_create(bytes=32)
	j = 0
	while nonEmpty and (j < threshold and use_threshold):
		landmarks = []
		keypoints = []
		features = []
		alias = entry[0]
		image = cv2.imread(image_base_path + alias, 3)
		shift_index = 0
		print("image: " + alias)
		for landmark in entry[2:]:
			coordinates = landmark.split('_')
			for i in range(len(coordinates)):
				# print(coordinates[i])
				coordinates[i] = float(coordinates[i])
			if coordinates[0] != -1:
				keypoints.append(cv2.KeyPoint(x=coordinates[0] + landmark_shifts[shift_index][2],
											  y=coordinates[1] + landmark_shifts[shift_index][1], _size=keypoint_size))
				min(int(coordinates[1]), int(coordinates[1] + 2 * landmark_shifts[shift_index][2]))
				shifted_position = [int(coordinates[1] + landmark_shifts[shift_index][1]),
									int(coordinates[0] + landmark_shifts[shift_index][2])]
				section = image[
						  int(shifted_position[0] - keypoint_size // 2): int(shifted_position[0] + keypoint_size // 2),
						  int(shifted_position[1] - keypoint_size // 2): int(shifted_position[1] + keypoint_size // 2)]
			# section = image[int(coordinates[1] - keypoint_size//2): int(coordinates[1] + keypoint_size//2), int(coordinates[0] - keypoint_size//2): int(coordinates[0] + keypoint_size//2)]
			# print(section)
			# print(shifted_position[0] - 4, shifted_position[0] + 4, shifted_position[1] - 4, shifted_position[1] + 4 )
			# print(landmark_shifts[shift_index][0])
			# cv2.imshow('ImageWindow', section)
			# cv2.waitKey(0)
			landmarks.append(coordinates[:-1])
			shift_index += 1
		kp, des = brief.compute(image, keypoints)
		imageData.append([alias, landmarks, des])

		# localAreas = []
		# for landmark in entry[2:]:
		# 	coordinates = landmark.split('_')
		# 	for i in range(len(coordinates)):
		# 		print(coordinates[i])
		# 		coordinates[i] = int(coordinates[i])
		j += 1
		try:
			entry = next(reader)
		except Exception as e:
			nonEmpty = False

	for data in imageData:
		writer.writerow(data)

	inputFile.close()

if __name__ == "__main__":
	execute()

