from flask import Flask, request, redirect, render_template, url_for
import requests
import json

app = Flask(__name__)

API_URL = 'https://apigerenciarusuarios.onrender.com/list/usuarios'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/lista/usuarios')
def lista_usuarios():
    resposta = requests.get(API_URL)
    usuarios = resposta.json()

    return render_template('list_usuarios.html', usuarios=usuarios)

@app.route('/usuario/<int:id>', methods=['PUT', 'GET'])
def ver_usuario_id(id):
    if request.method == 'PUT':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        funcao = request.form['funcao']

        params = {
            'nome': nome,
            'email': email,
            'senha': senha,
            'funcao': funcao,
        }

        response = requests.put(f'https://apigerenciarusuarios.onrender.com/edit/usuario/{id}', params=params)
        print(f'{response.json()}')
        return redirect(url_for('ver_usuario_id', id=id))

    try:
        usuario_id = requests.get(f'https://apigerenciarusuarios.onrender.com/usuarios/{id}')
        usuarios = usuario_id.json()
    except Exception as e:
        return f"Erro ao acessar este usuário: {str(e)}"
    return render_template('usuario.html', usuarios=usuarios)


@app.route('/register/usuario', methods=['POST','GET'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        funcao = request.form['funcao']

        params = {
            'nome': nome,
            'email': email,
            'senha': senha,
            'funcao': funcao
        }

        response = requests.post('https://apigerenciarusuarios.onrender.com/post/usuario', params=params)
        print(f"{response.json()}")
        return redirect('/register/usuario')
    return render_template('cadastro.html')

@app.route('/deletar/<int:id>', methods=['DELET', 'GET'])
def deletar_usuario(id):
    response = requests.delete(f'https://apigerenciarusuarios.onrender.com/delet/usuarios/{id}', params={
        'id': id
    })
    print(f'{response.json()}')
    return redirect(url_for('lista_usuarios'))



app.run(host="0.0.0.0", port=8080)
