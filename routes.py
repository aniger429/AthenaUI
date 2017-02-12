import pandas as pd
from flask import Flask, render_template, send_from_directory
from controllers import uploadFile
import os
# Initialize the Flask application
app = Flask(__name__)
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'data/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['csv', 'xls', 'xlsx'])


@app.route('/')
def home():
    return render_template("base.html")

@app.route('/datacleaning')
def datacleaning():
    return render_template("datacleaning.html")

@app.route('/chart-view')
def chartView():
    return render_template("chart-view.html")

# @app.route('/test')
# def displayTable():
#     data = pd.read_excel('/home/dudegrim/Google Drive/Thesis/Election Data/Election-18.xlsx')
#     return render_template('test.html', tables=[data.to_html()],
#                            titles=['na', 'Tweetsss'])

@app.route('/test')
def displayTable():
    return render_template('test.html')

# # This route will show a form to perform an AJAX request
# # jQuery is loaded to execute the request and update the
# # value of the operation
# @app.route('/')
# def index():
#     return render_template('test.html')

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    script_path = os.path.dirname(__file__)
    directoryPath = os.path.join(script_path, app.config['UPLOAD_FOLDER'])

    return uploadFile.upload(directoryPath, app.config['ALLOWED_EXTENSIONS'])

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user data
# an image, that image is going to be show after the upload
@app.route('/data/<filename>')
def uploaded_file(filename):
    print(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ == '__main__':
    app.run(
        debug=True
    )
