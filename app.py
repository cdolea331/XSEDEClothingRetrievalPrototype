from scipy.spatial.distance import cosine
import csv
import cv2
import numpy as np
from flask import Flask, request, redirect, render_template, url_for, send_from_directory, render_template
from werkzeug import secure_filename
import landmark_based_feature_extraction as feature_extraction
import landmark_based_retrieval as retrieval
import os
import cpn_landmark_detection.convert_tfrecords as conversion
import cpn_landmark_detection.eval_all_cpn_onepass as evaluation
lower_execution_time = True
retrieval_dataset_path ="Data/blouseData/"
UPLOAD_FOLDER = './cpn_landmark_detection/DATA/extracted/test_1'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER + '/Images/blouse', filename))
            new_csv = open("test.csv" , 'w')
            new_csv.write('image_id,image_category,\n')
            new_csv.write('Images/blouse/' + filename + ",blouse")
            conversion.convert_server()
            evaluation.make_predictions()
            feature_extraction.execute(image_base_path=UPLOAD_FOLDER, annotations_path="cpn_landmark_detection/seresnext50_cpn_blouse.csv",
                                       use_threshold=lower_execution_time)
            retrieval.execute(input_path="cpn_landmark_detection/seresnext50_cpn_blouse.csv")
            results = open("results.csv", 'r')
            results_csv = csv.reader(results)
            return_images = []
            line = next(results_csv)
            for i in range(5):
                return_images.append(retrieval_dataset_path + line[0])
                line = next(results_csv)
            # test_path = "Data/blouseData/Images/blouse/"
            # return_images = ["0a1f3a0ba8f1ae6e1e2b63972b9a4c73.jpg",'0a1f93208b8b45637648687efd75f61d.jpg','0a2ba658afc088e039d93fe67a266f9f.jpg',
            #                  '0a2cc8046ffdcf7635c490e0e34d0817.jpg','0a02d1f1a99aede99cca75b45efc5910.jpg']
            # for i in range(len(return_images)):
            #     return_images[i] = test_path + return_images[i]
            # print(return_images)
            return redirect(url_for('uploaded_file', filename = UPLOAD_FOLDER[2:] + '/Images/blouse/' + filename, files = return_images))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/showresults')
def uploaded_file():

    filename = request.args.get('filename')
    files = request.args.getlist('files')
    # print(len(files))
    filename = 'http://127.0.0.1:5000/' + filename
    # print(filename)
    for i in range(len(files)):
        files[i] = 'http://127.0.0.1:5000/' + files[i]
        # print(files[i])
        # print(filename)

    return render_template('template.html', filename=filename, file0=files[0],file1=files[1],file2=files[2],file3=files[3],file4=files[4])



@app.route('/cpn_landmark_detection/DATA/extracted/test_1/Images/blouse/<filename>')
def original_file(filename):
    return send_from_directory('cpn_landmark_detection/DATA/extracted/test_1/Images/blouse', filename)

@app.route('/Data/blouseData/Images/blouse/<filename>')
def new_file(filename):

    return send_from_directory('Data/blouseData/Images/blouse', filename)

if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/Testing/Data/uploads/<filename>')
# def send_file(filename):
#
#     return send_from_directory('Testing/Data/uploads', filename)
