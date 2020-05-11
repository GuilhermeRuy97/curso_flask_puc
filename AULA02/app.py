from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import threading
import os
from os import listdir
from os.path import isfile, join
import getpass

mypath = '/home/walter/Documentos/curso_flask_puc/AULA02/downloads'
username = getpass.getuser()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def uploadFiles():    
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload_files.html', username=username)

        files = request.files.getlist('file')

        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(mypath, filename))

        
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        #threadObj = threading.Thread(target=calcula(username))
        #threadObj.start()
        #return redirect('/relatorio')
        return render_template('relatorio.html', onlyfiles=onlyfiles, username=username)

    return render_template('upload_files.html', username=username)

@app.route('/download', methods=['GET', 'POST'])
def downloadFile ():
    if request.method == 'POST':
        filename = request.form['filename']

        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        if 'filename' not in request.form:
            return render_template('upload_files.html', username=username, onlyfiles=onlyfiles)
          
        path = "downloads/"+filename
        return send_file(path, as_attachment=True)
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return render_template('download_file.html', username=username, onlyfiles=onlyfiles)

def calcula(username):    
    pass

if __name__ == "__main__":
    app.run()
