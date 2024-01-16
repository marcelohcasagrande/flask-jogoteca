from jogoteca import app
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash

@app.route( '/login' ) # rota de login.
def login():
    proxima = request.args.get( 'proxima' ) # dando um get para ele ir para a próxima.
    form = FormularioUsuario() # pegando formulário de usário do helpers.
    return render_template( 'login.html', proxima = proxima, form = form ) # redirecionando passando o form.

@app.route( '/autenticar', methods = [ 'POST', ] ) # autenticação. Precisa usar o method post para pegar as infos.
def autenticar():
    form = FormularioUsuario( request.form ) # requisitando formulário.
    usuario = Usuarios.query.filter_by( nickname = form.nickname.data ).first() # vendo se existe o usuário.
    senha = check_password_hash( usuario.senha, form.senha.data ) # checando a senha.
    if usuario and senha: # se os dois forem verdadeiros...
        session[ 'usuario_logado' ] = usuario.nickname # loga usuário.
        flash( usuario.nickname + ' logado com sucesso!' ) # mensagem do Flask (usando flash).
        proxima_pagina = request.form[ 'proxima' ] # pegando próxima.
        return redirect( proxima_pagina ) # redirecionando para a próxima.
    else:
        flash( 'Usuário não logado.' ) # caso não logar, voltar em login.
        return redirect( url_for( 'login' ) ) # usando URL FOR para ele ir para a função de login (def login).

@app.route( '/logout' ) # rota para deslogar.
def logout():
    session[ 'usuario_logado' ] = None # setando para deslogar.
    flash( 'Logout efetuado com sucesso!' ) # mensagem do Flask (usando flash).
    return redirect( url_for( 'index' ) ) # redirecionando para def index.