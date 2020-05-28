
'''
EXECUTAR PARA INICIAR O XAMPP:      
sudo /opt/lampp/manager-linux-x64.run
'''

from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
import os
import re
import json
from os import listdir
from os.path import isfile, join
import getpass
import time
import requests
import bs4     # pip install beautifulsoup4 requests
import mysql.connector    # pip install mysql-connector-python

# path de onde arquivo sera salvo
mypath = '/home/flaskman/Documentos/curso_flask_puc/AULA03/downloads'
username = getpass.getuser()

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def uploadFiles():
    '''
    Descricao: essa rota direciona a requisicao para uma pagina de upload de arquivos.
    '''
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload_files.html', username=username)

        files = request.files.getlist('file')

        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(mypath, filename))

        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        return render_template('relatorio.html', onlyfiles=onlyfiles, username=username)

    return render_template('upload_files.html', username=username)


@app.route('/download', methods=['GET', 'POST'])
def downloadFiles():
    '''
    Descricao: essa rota direciona a requisicao para uma pagina de upload de arquivos.
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
def climaTempo():
    '''
    Descricao: essa rota direciona a requisicao para recuperacao de dados do site Clima Tempo
    para a cidade de Pocos de Caldas.
    '''
    if request.method == 'GET':

        url = 'https://www.climatempo.com.br/previsao-do-tempo/cidade/182/pocosdecaldas-mg'
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        temp_min = soup.find(id='min-temp-1')
        #print("Temperatura minima: " + temp_min.contents[0])

        temp_max = soup.find(id='max-temp-1')
        #print("Temperatura maxima: " + temp_max.contents[0])

        text = soup.find(class_='variables-list').get_text()
        text = re.sub("\n", " ", text)
        # print(text)

        var = text.split(" ")
        #print("lista suja: " + str(var))

        new_list = []

        for item in var:
            if item != "":
                new_list.append(item)

        #print("nova lista: " + str(new_list))

        primeiro_dado = str(
            new_list[0] + " - min: " + new_list[1] + " max: " + new_list[2])
        segundo_dado = str(new_list[3] + " - mm: " +
                           new_list[4] + " - prob: " + new_list[6])
        terceiro_dado = str(
            new_list[7] + " - dir: " + new_list[8] + " - int: " + new_list[10])
        quarto_dado = str(
            new_list[11] + " - min: " + new_list[12] + " - max: " + new_list[13])
        quinto_dado = str(
            new_list[14] + " - nascS: " + new_list[15] + " - porS: " + new_list[16])
        json_object = json.loads('{ "primeiro_dado": "%s", \
                                    "segundo_dado": "%s", \
                                    "terceiro_dado": "%s", \
                                    "quarto_dado": "%s", \
									"quinto_dado": "%s"}' % (primeiro_dado, segundo_dado,
                                  terceiro_dado, quarto_dado, quinto_dado))
        json_formatted_str = json.dumps(json_object, indent=2)
        print(json_formatted_str)

        return jsonify({"status": "ok", "method": "GET", "return": json_formatted_str}), 200
        # return primeiro_dado
    return jsonify({"status": "ok", "method": "POST", "return": "metodo post"}), 200


@app.route('/bd', methods=['GET', 'POST'])
def bancoDados():
    '''
    Descricao: essa rota direciona a requisicao para uma pagina de estudo de banco de dados.
    '''
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test")

    # print(mydb)

    mycursor = mydb.cursor()

    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
        print(x)

    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print(x)

    mycursor.execute("CREATE DATABASE if not exists curso_flask")

    return "acessando o banco..."


@app.route('/atualiza_cadastro', methods=['GET', 'POST'])
def atualiza_cadastro():
    '''
    Descricao: essa rota direciona a requisicao para uma pagina de atualizacao de dados no BD.
    '''
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="curso_flask")

    mycursor = mydb.cursor()
    #username = getpass.getuser()
    username = "flaskman"
    msg = ''
    if username:

        if request.method == 'POST' and 'nome' in request.form:

            nome = request.form['nome']

            if not re.match(r'[A-Za-z]+', nome):
                msg = 'Nome deve conter somente caracteres!'

            else:

                sql = "UPDATE usuarios SET nome = %s where login = %s"
                val = (nome, username)
                mycursor.execute(sql, val)
                mydb.commit()
            print(msg)

        if request.method == 'POST' and 'sobrenome' in request.form:

            sobrenome = request.form['sobrenome']

            if not re.match(r'[A-Za-z]+', sobrenome):
                msg = 'Sobrenome deve conter somente caracteres!'

            else:

                sql = "UPDATE usuarios SET sobrenome = %s where login = %s"
                val = (sobrenome, username)
                mycursor.execute(sql, val)
                mydb.commit()
            print(msg)

        if request.method == 'POST' and 'email' in request.form:

            email = request.form['email']

            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Email deve conter o padrao de email!'

            else:

                sql = "UPDATE usuarios SET email = %s where login = %s"
                val = (email, username)
                mycursor.execute(sql, val)
                mydb.commit()
            print(msg)

        if request.method == 'POST' and 'tel01' in request.form:

            tel01 = request.form['tel01']

            if not re.match(r'[0-9]+', tel01):
                msg = 'Tel 01 deve conter somente numeros!'
            else:

                sql = "UPDATE usuarios SET tel01 = %s where login = %s"
                val = (tel01, username)
                mycursor.execute(sql, val)
                mydb.commit()
            print(msg)

        if request.method == 'POST' and 'rg' in request.form:

            rg = request.form['rg']

            if not re.match(r'[0-9]+', rg):
                msg = 'rg deve conter somente numeros!'
            else:

                sql = "UPDATE usuarios SET rg = %s where login = %s"
                val = (rg, username)
                mycursor.execute(sql, val)
                mydb.commit()
            print(msg)

        mycursor.close()
        time.sleep(1)
        return render_template('atualiza_cadastro.html', msg=msg, username=username)
    return render_template('atualiza_cadastro.html', msg=msg, username=username)

