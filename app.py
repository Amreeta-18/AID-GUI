# Libraries
import os
from flask import Flask, flash, request, redirect, url_for, render_template, make_response, send_file
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
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Utility - Checks whether the file type is supported
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# App main page
@app.route("/result", methods=['POST'])
def result():
    if request.method == 'POST':
        usecase = request.form['usecase']
        subgoal = request.form['subgoal'].lower()
        action = request.form['action'].lower()
        flag1, flag2 = 0, 0
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

        rep = open("Upload/report.csv", "w")
        rep.write("Use case, Subgoal, Action, Filename, Rule 1, Rule 2, Rule 3\n")
        if file and allowed_file(file.filename):
            # Get filename and pass to backend
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            output, flag1, flags1 = AID.MainProcess(usecase, subgoal, action, f"Upload/{filename}", 1)
            flags = ",".join(flags1)
            row = f"{usecase}, {subgoal}, {action}, {filename}, {flags}\n"
            rep.write(row)
        else:
            return render_template('error.html')
        # get file2
        file = request.files['html_file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Get filename and pass to backend
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            output2, flag2, flags2 = AID.MainProcess(usecase, subgoal, action, f"Upload/{filename}", 2)
            flags = ",".join(flags2)
            row = f"{usecase}, {subgoal}, {action}, {filename}, {flags}\n"
            rep.write(row)
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
        else:
            return render_template('error.html')
            
        rep.close()
        return render_template('result.html', output = flag1, output2 = flag2)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Functionality pages
@app.route('/demopage')
def demopage():
    return render_template('demopage.html')

@app.route('/uploadpage', methods=['POST'])
def uploadpage():
    if request.method == 'POST':
        Identity = request.form['Identity']
        Affiliation = request.form['Affiliation'].lower()
        comment = request.form['comment'].lower()
        f = open("User_data/data.txt", "a")
        f.write(f"Identity = {Identity}, Affiliation = {Affiliation}, comment = {comment}\n")
        # print(Identity, Affiliation, comment)
    return render_template('uploadpage.html')

@app.route('/highlight1')
def highlightpage1():
    response = make_response(render_template('highlight1.html'))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0" # Proxies.
    return response

@app.route('/highlight2')
def highlightpage2():
    return render_template('highlight2.html')

@app.route('/download')
def downloadFile ():
    path = "Upload/report.csv"
    return send_file(path, as_attachment=True)#, download_name="report.csv")

if __name__=="__main__":
    app.run(debug=True)