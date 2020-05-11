from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import threading
import os

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello():
    username = 'Walter'
    #return render_template('upload_files.html', username=username)
    if request.method == 'POST':
        if 'file' not in request.files:
            #return redirect(url_for('/'))
            render_template('upload_files.html')

        files = request.files.getlist('file')

        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join('/home/walter/Documentos/curso_flask_puc/AULA02/downloads', filename))

        #flash('Arquivo enviado com successo')
        threadObj = threading.Thread(target=calcula(username))
        threadObj.start()
        #return redirect('/relatorio')
        return render_template('relatorio.html')

    return render_template('upload_files.html')

def calcula(username):
    print('calculando...')
    pass

if __name__ == "__main__":
    app.run()
