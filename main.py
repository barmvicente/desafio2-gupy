import crcmod.predefined
from flask import Flask, request, abort, redirect
from jinja2 import Environment, FileSystemLoader
from os import path


def shorten_url(url):
    '''Fuanco que recebe uma url e retorna encurtada'''

    url_hash = crcmod.predefined.mkCrcFun('crc-32')
    hex_url_hash = str(hex(url_hash(url)))[:-1]

    return dec_to_base62(int(hex_url_hash, 16))


def dec_to_base62(dec_url):
    '''Funcao que recebe um decimal e o converte para a base 62'''

    figures = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if dec_url == 0:
        return figures[0]
    base62 = []

    while dec_url:
        rem = dec_url % 62
        dec_url = dec_url // 62
        base62.append(figures[rem])

    base62.reverse()

    return ''.join(base62)


app = Flask(__name__)
record = {}

arq = open('record.txt', 'r')  # abrindo o arquivo para leitura
record = eval(arq.read())  # Lendo o dicionario contido no arquivo
arq.close()  # fechando o arquivo lido


@app.route('/')
def index():
    '''Funcao que carrega o template'''
    env = Environment(loader=FileSystemLoader(path.dirname(path.abspath(__file__))))
    template = env.get_template('main.html')
    data = []
    for item in record:
        linha = []
        linha.append(item)
        linha.extend(record[item])
        data.append(linha)

    ordened_data = sorted(data, key=lambda x: x[2], reverse=True)

    return template.render(record=ordened_data[:10])


@app.route('/api/shorten', methods=['POST'])
def short():
    '''Funcao que processa a requisicao do formulario'''
    return shorten(request.form['url'])


@app.route('/shorten/<string:url>')
def shorten(url):
    '''Funcao que calcula a url encurtada e escreve no arquivo'''
    global record
    short = shorten_url(url)

    if short in record:
        record[short][1] += 1
    else:
        record[short] = [url, 1]

    arq = open('record.txt', 'w')  # Abrindo o arquivo para escrita
    arq.write(str(record))  # Escrevendo o dicionario
    arq.close()  # Fechando o arquivo

    print record
    return 'http://127.0.0.1:5000/a/' + short

@app.route('/a/<string:hash>')
def browse(hash):
    '''Funcao que faz a url curta apontar para o url longa'''
    global record
    long_url = record[hash][0]
    if long_url[0:4] != 'http':
        long_url = 'http://' + long_url
    return redirect(long_url, code=302)

if __name__ == '__main__':
    app.run(debug=True)
