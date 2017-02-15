from flask import Flask, render_template, send_from_directory
from controllers import uploadFile
import os
from DBModels.Data import *
from controllers.DataCleaning import cleaning

# Initialize the Flask application
app = Flask(__name__)
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'Data/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['csv', 'xls', 'xlsx'])


@app.route('/')
def home():
    return render_template("base.html")


@app.route('/data_cleaning')
def data_cleaning():
    return render_template("datacleaning.html", dataFileList=getAllData())


@app.route('/data_cleaning/<filename>')
def clean_file(filename):
    script_path = os.path.dirname(__file__)
    file_path = os.path.join(script_path, app.config['UPLOAD_FOLDER'], filename)
    cleaning.cleaning_file(file_path)
    tweet_cleaned(filename)
    return render_template("datacleaning.html", dataFileList=getAllData())


@app.route('/chart-view')
def chart_view():
    return render_template("chart-view.html")


@app.route('/test')
def display_table():
    return render_template('test.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    script_path = os.path.dirname(__file__)
    directoryPath = os.path.join(script_path, app.config['UPLOAD_FOLDER'])

    return uploadFile.upload(directoryPath, app.config['ALLOWED_EXTENSIONS'])

if __name__ == '__main__':
    app.run(
        debug=True
    )
