# Libraries
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import requests

# Backend Integration
import MainTool

# Server upload location
UPLOAD_FOLDER = 'Upload'

# Allowed file types
ALLOWED_EXTENSIONS = {'xlsx'}

# Flask Configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Utility - Checks whether the file type is supported
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# App main page
@app.route("/result", methods=['POST'])
def result():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # get file
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # If uploaded file and file type is good to go
        if file and allowed_file(file.filename):
            # Get filename and pass to backend
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Backend output
            output = str(MainTool.MainProcess(f"Upload/{filename}"))
            # Download option to end user

            # Rerender on html
            return render_template('result.html', output = output)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Functionality page
@app.route('/uploadpage')
def uploadpage():
    return render_template('uploadpage.html')

if __name__=="__main__":
    app.run(debug=True)