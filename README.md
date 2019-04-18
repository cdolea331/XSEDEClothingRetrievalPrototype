# XSEDEClothingRetrievalPrototype
A progenitor to future, more effective models utilizing landmarks for clothing retrieval

To utilize this code:
This must be run on a machine with a GPU with a large amount of VRAM(~6-8GB) as it contains a large deep learning model.

To run this server, first download the Tianchi FashionAI Global Challenge 2018 - Key Points Detection of Apparel dataset or another keypoints detection dataset and place the images inside the cpn_landmark_detection folder's data directory's extracted directory as such
```
DATA_DIR/
 	   |->train_0/
 	   |    |->Annotations/
 	   |    |    |->annotations.csv
 	   |    |->Images/
 	   |    |    |->blouse
 	   |    |    |->...
 	   |->train_1/
 	   |    |->Annotations/
 	   |    |    |->annotations.csv
 	   |    |->Images/
 	   |    |    |->blouse
 	   |    |    |->...
 	   |->...
 	   |->test_0/
 	   |    |->test.csv
 	   |    |->Images/
 	   |    |    |->blouse
 	   |    |    |->...
  ```   
Use convert_tfrecords to convert the data into tfrecords for training, then use Then run train_senet_onebyone to train.

After training, remove the training/testing images(not the folders) and empty the .csv files.

Now simply run app.py and upload an image when prompted after accessing the server via a browser.

Requires: Flask, Pandas, Numpy, Scipy, Tensorflow

