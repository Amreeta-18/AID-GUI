# Libraries
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import requests

# Backend Integration
import AID

# Server upload location
UPLOAD_FOLDER = 'Upload'

# Allowed file types
ALLOWED_EXTENSIONS = {'xlsx', 'html'}

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
        usecase = request.form['usecase']
        subgoal = request.form['subgoal']
        action = request.form['action']
        # check if the post request has the file part
        if 'html_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        if 'html_files' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # get file1
        file = request.files['html_files']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Get filename and pass to backend
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            output = AID.MainProcess(usecase, subgoal, action, f"Upload/{filename}", 1)

        # get file2
        file = request.files['html_file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Get filename and pass to backend
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            output2 = AID.MainProcess(usecase, subgoal, action, f"Upload/{filename}", 2)

            # Backend output
            # output = str(MainTool.MainProcess(f"Upload/{filename}"))
            # output = str(linkParser.txtForm(file = f"Upload/{filename}"))

            # output2 = "A"
            # output2 = AID.MainProcess(usecase, subgoal, action, f"Upload/{filename2}", 2)
            # output = str(textParser.textParse2(f"Upload/{filename}"))
            # Download option to end user
            # output = f"{output}\nSubgoal: {subgoal} \nAction: {action}"
            # Rerender on html
            # output = output.replace("\n", "<br")
        return render_template('result.html', output = output, output2 = output2)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Functionality pages
@app.route('/uploadpage')
def uploadpage():
    return render_template('uploadpage.html')

@app.route('/highlight1')
def highlightpage1():
    return render_template('Highlight/changed1.html')

@app.route('/highlight2')
def highlightpage2():
    return render_template('Highlight/changed2.html')

if __name__=="__main__":
    app.run(debug=True)