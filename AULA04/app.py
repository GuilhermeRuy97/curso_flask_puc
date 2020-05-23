
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

mypath = '/home/flaskman/Documentos/curso_flask_puc/AULA04/downloads'  # path de onde arquivo sera salvo
username = getpass.getuser()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def uploadFiles():
    '''
    Descricao da classe: essa rota direciona a requisicao para uma pagina de upload de arquivos.
    '''    
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload_files.html', username=username)

        files = request.files.getlist('file')

        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(mypath, filename))

        
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        threadObj = threading.Thread(target=calcula(username))
        threadObj.start()
        #return redirect('/relatorio')
        return render_template('relatorio.html', onlyfiles=onlyfiles, username=username)

    return render_template('upload_files.html', username=username)

@app.route('/download', methods=['GET', 'POST'])
def downloadFile ():
    '''
    Descricao da classe: essa rota direciona a requisicao para uma pagina de upload de arquivos.
    '''
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
    '''
    Descricao da classe: essa classe direciona a requisicao para recuperacao de dados do site Clima Tempo
    para a cidade de Pocos de Caldas.
    '''
    if request.method == 'GET':

        url = 'https://www.climatempo.com.br/previsao-do-tempo/cidade/182/pocosdecaldas-mg'
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        temp_min = soup.find(id='min-temp-1')
        print("Temperatura minima: " + temp_min.contents[0])

        temp_max = soup.find(id='max-temp-1')
        print("Temperatura maxima: " + temp_max.contents[0])

        text = soup.find(class_='variables-list').get_text()
        text = re.sub("\n", " ", text)
        print(text)

        var = text.split(" ")
        print("lista suja: " + str(var))

        new_list = []

        for item in var:
            if item != "":
                new_list.append(item)
        
        print("nova lista: " + str(new_list))
     
        
        primeiro_dado = str(new_list[0] + " - min: " + new_list[1] + " max: " + new_list[2])
        segundo_dado = "2"#str(new_list[1] + " : " + new_list[1] + " : " + new_list[2])
        terceiro_dado = "3"#str(new_list[2] + " : " + new_list[2] + " : " + new_list[3])
        quarto_dado = "4"#str(new_list[3] + " : " + new_list[3] + " : " + new_list[4])

        json_object = json.loads('{ "primeiro_dado": "%s", \
                                    "segundo_dado": "%s", \
                                    "terceiro_dado": "%s", \
                                    "quarto_dado": "%s"}' % (primeiro_dado, segundo_dado, terceiro_dado, quarto_dado ))
        json_formatted_str = json.dumps(json_object, indent=2)
        print(json_formatted_str)
        
        return jsonify({"status": "ok", "method": "GET", "return": json_formatted_str}), 200
        #return primeiro_dado
    return jsonify({"status": "ok", "method": "POST", "return": "metodo post"}), 200


@app.route('/bd', methods=['GET', 'POST'])
def bancoDados():
    '''
    Descricao da classe: essa rota direciona a requisicao para uma pagina de estudo de banco de dados.
    '''
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
    Desc: Metodo verificador de erro na requisicao para request nao compreendida.
    """
    return jsonify({"status": "not ok", "message": "this server could not understand your request"}), 400


@app.errorhandler(404)
def not_found(e):
    """
    Desc: Metodo verificador de erro na requisicao para rota nao encontrada.      
    """
    return jsonify({"status": "not found", "message": "route not found"}), 404


@app.errorhandler(500)
def not_found2(e):
    """
    Desc: Metodo verificador de erro na requisicao de erro de servidor.      
    """  
    return jsonify({"status": "internal error", "message": "internal error occurred in server"}), 500


def calcula(username): 
    """
    Desc: metodo exemplo de thread.
    """   
    print("executando uma thread...")
    #pass

