import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import requests
import MainTool

UPLOAD_FOLDER = 'Upload'
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/result", methods=['POST'])
def result():
    if request.method == 'POST':
        # # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            output = str(MainTool.MainProcess(f"Upload/{filename}"))
            return render_template('result.html', output = output)

@app.route('/')
def home():
    return render_template('firstpage.html')


@app.route('/uploadpage')
def uploadpage():
    return render_template('uploadpage.html')

# @app.route("/result", methods=['POST'])
# def result():
#     if request.method == 'POST':
#         # doc = request.form['WEB']# Take the xl file from front end
#         # save xl file in server as "inp.xlsx"
#         output = str(MainTool.MainProcess("Example_input.xlsx"))
#         # Download option to end user
#         return render_template('result.html', output = output)

if __name__=="__main__":
    app.run(debug=True)