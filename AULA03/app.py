
'''
EXECUTAR PARA INICIAR O XAMPP:      
sudo /opt/lampp/manager-linux-x64.run
'''

from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
import threading
import os, re, json
from os import listdir
from os.path import isfile, join
import getpass
import requests, bs4     # pip install beautifulsoup4 requests
import mysql.connector    # pip install mysql-connector-python

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

@app.route('/weather', methods=['GET', 'POST'])
def climaTempo ():
    if request.method == 'GET':

        url = 'https://www.climatempo.com.br/previsao-do-tempo/cidade/182/pocosdecaldas-mg'
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        temp_min = soup.find(class_='min-temp')
        print("Temperatura minima: " + temp_min.contents[0])

        temp_max = soup.find(class_='max-temp')
        print("Temperatura maxima: " + temp_max.contents[0])

        text = soup.find(class_='-gray _flex _align-center').get_text()
        text = re.sub("\n", "", text)
        print("mm de chuva: " + text)

        text = soup.find_all(class_='list _margin-t-20')

        var = text[0].get_text().split()
        var2 = text[1].get_text().split()
        var3 = text[2].get_text().split()

        print(var[0] + " : " + var2[0] + " : " + var3[0] + var3[1])
        print(var[1] + " : " + var2[1] + " : " + var3[2])
        print(var[2] + " : " + var2[2] + " : " + var3[3])
        print(var[3] + " : " + var2[3] + " : " + var3[4])
        #return "tempo de quarentena..."
        
        primeiro_dado = str(var[0] + " : " + var2[0] + " : " + var3[0] + var3[1])
        segundo_dado = str(var[1] + " : " + var2[1] + " : " + var3[2])
        terceiro_dado = str(var[2] + " : " + var2[2] + " : " + var3[3])
        quarto_dado = str(var[3] + " : " + var2[3] + " : " + var3[4])

        json_object = json.loads('{ "primeiro_dado": "%s", \
                                    "segundo_dado": "%s", \
                                    "terceiro_dado": "%s", \
                                    "quarto_dado": "%s"}' % (primeiro_dado, segundo_dado, terceiro_dado, quarto_dado ))
        json_formatted_str = json.dumps(json_object, indent=2)
        print(json_formatted_str)

        return jsonify({"status": "ok", "method": "GET", "return": json_formatted_str}), 200
    return jsonify({"status": "ok", "method": "POST", "return": "metodo post"}), 200


@app.route('/bd', methods=['GET', 'POST'])
def bancoDados():
    mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="",
	database="test")

    #print(mydb)

    mycursor = mydb.cursor()

    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
    	print(x)
    
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print(x)   

    mycursor.execute("CREATE DATABASE if not exists test2")

    return "acessando o banco..."

@app.errorhandler(400)
def bad_request(e):
    """
    Desc: Metodo verificador de erro na requisicao.
    """
    return jsonify({"status": "not ok", "message": "this server could not understand your request"}), 400


@app.errorhandler(404)
def not_found(e):
    """
    Desc: Metodo verificador de erro na requisicao.  
    
    """
    return jsonify({"status": "not found", "message": "route not found"}), 404


@app.errorhandler(500)
def not_found2(e):
    """
    Desc: Metodo verificador de erro na requisicao.  
    
    """  
    return jsonify({"status": "internal error", "message": "internal error occurred in server"}), 500




def calcula(username):    
    pass

