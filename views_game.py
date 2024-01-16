from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo
import time

@app.route( '/' ) # rota inicial.
def index():
    lista = Jogos.query.order_by( Jogos.id ) # lista de jogos da classe Jogos.
    return render_template( 'lista.html', titulo = 'Jogos', jogos = lista ) # passando a lista para a página HTML.

@app.route( '/novo' ) # rota para adicionar jogo.
def novo():
    if 'usuario_logado' not in session or session[ 'usuario_logado' ] == None: # checa se usuário está logado.
        return redirect( url_for( 'login', proxima = url_for( 'novo' ) ) ) # caso não esteja, vai para login e depois para novo.
    form = FormularioJogo() # puxando formulário de jogo do helpers.
    return render_template( 'novo.html', titulo = 'Novo Jogo', form = form ) # redirecionando passando o form.

@app.route( '/criar', methods = [ 'POST', ] )
def criar():
    form = FormularioJogo( request.form ) # requisitando formulário.

    if not form.validate_on_submit(): # caso não esteja validado os formulários preenchidos, volta para novo.
        return redirect( url_for( 'novo' ) )

    nome = form.nome.data # puxando nome.
    categoria = form.categoria.data # puxando categoria.
    console = form.console.data # puxando console.

    jogo = Jogos.query.filter_by( nome = nome ).first() # analisando se o jogo já existe pelo nome.

    if jogo: # caso exista, mensagem e volta para o index.
        flash( 'Jogo já existente!' )
        return redirect( url_for( 'index' ) )

    novo_jogo = Jogos( nome = nome, categoria = categoria, console = console ) # caso não exista, cria o objeto.
    db.session.add( novo_jogo ) # adiciona ao DB.
    db.session.commit() # commita.

    arquivo = request.files[ 'arquivo' ] # pegando a imagem do jogo que foi passada.
    upload_path = app.config[ 'UPLOAD_PATH' ] # diretório para salvar a imagem.
    timestamp = time.time() # criando uma data em milisegundos para que os nomes sejam distintos.
    arquivo.save( f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg' ) # salvando.

    return redirect( url_for( 'index' ) ) # volta para index.

@app.route( '/editar/<int:id>' ) # rota para editar, puxando o id do jogo a ser editado.
def editar( id ):
    if 'usuario_logado' not in session or session[ 'usuario_logado' ] == None: # checa se usuário está logado.
        return redirect( url_for( 'login', proxima = url_for( 'editar', id = id ) ) ) # caso não esteja, vai para login e depois para editar o jogo do id.
    jogo = Jogos.query.filter_by( id = id ).first() # checa o jogo a ser editado na classe jogos.
    form = FormularioJogo() # puxando formulário de jogo do helpers.
    form.nome.data = jogo.nome # pegando nome atual para o id.
    form.categoria.data = jogo.categoria # pegando categoria atual para o id.
    form.console.data = jogo.console # pegando console atual para o id.
    capa_jogo = recupera_imagem( id ) # pegando capa do jogo atual para o id.
    return render_template( 'editar.html', titulo = 'Editando Jogo', id = id, capa_jogo = capa_jogo, form = form ) # redireciona para editar.html passando infos.

@app.route( '/atualizar', methods = [ 'POST', ] ) # atualização. Precisa usar o method post para pegar as infos.
def atualizar():
    form = FormularioJogo( request.form ) # puxando informações do formulário.

    if form.validate_on_submit(): # caso seja validado o preenchimento do formulário.
        jogo = Jogos.query.filter_by( id = request.form[ 'id' ] ).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add( jogo ) # atualiza infos.
        db.session.commit() # commita.

        arquivo = request.files[ 'arquivo' ] 
        upload_path = app.config[ 'UPLOAD_PATH' ]
        timestamp = time.time()
        deleta_arquivo( id )
        arquivo.save( f'{upload_path}/capa{jogo.id}-{timestamp}.jpg' ) # atualiza imagem do jogo deletando a imagem anterior do banco de dados de imagens.

    return redirect( url_for( 'index' ) ) # voltando para index.

@app.route( '/deletar/<int:id>' ) # rota para deletar.
def deletar( id ):
    if 'usuario_logado' not in session or session[ 'usuario_logado' ] == None: # checa se usuário está logado.
        return redirect( url_for( 'login' ) ) # caso não esteja, vá até login.

    Jogos.query.filter_by( id = id ).delete() # deletando jogo de interesse.
    db.session.commit() # commitando.
    flash( 'Jogo deletado com sucesso!' ) # mensagem para formalizar que o jogo foi deletado.

    return redirect( url_for( 'index' ) ) # voltando para index.

@app.route( '/uploads/<nome_arquivo>' ) # rota para mandar imagem do jogo para a pasta de uploads.
def imagem( nome_arquivo ):
    return send_from_directory( 'uploads', nome_arquivo )