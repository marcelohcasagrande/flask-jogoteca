import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators

class FormularioJogo( FlaskForm ): # usa o Flask WTF para montar formulários e o WtForms para formatar campos.
    nome = StringField( 'Nome do Jogo', [ validators.DataRequired(), validators.Length( min = 1, max = 50 ) ] ) # exige preenchimento e quantidade mínimas e máximas.
    categoria = StringField( 'Categoria', [ validators.DataRequired(), validators.Length( min = 1, max = 40 ) ] )  # exige preenchimento e quantidade mínimas e máximas.
    console = StringField( 'Console', [ validators.DataRequired(), validators.Length( min = 1, max = 20 ) ] )  # exige preenchimento e quantidade mínimas e máximas.
    salvar = SubmitField( 'Salvar' )

class FormularioUsuario( FlaskForm ): # usa o Flask WTF para montar formulários.
    nickname = StringField( 'Nickname', [ validators.DataRequired(), validators.Length( min = 1, max = 8 ) ] )  # exige preenchimento e quantidade mínimas e máximas.
    senha = PasswordField( 'Senha', [ validators.DataRequired(), validators.Length( min = 1, max = 100 ) ] )  # exige preenchimento e quantidade mínimas e máximas.
    login = SubmitField( 'Login' )

def recupera_imagem( id ): # Busca imagem.
    for nome_arquivo in os.listdir( app.config[ 'UPLOAD_PATH' ] ):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa_padrao.jpg'

def deleta_arquivo( id ): # Deleta imagem anterior quando estamos atualizando a imagem de um jogo.
    arquivo = recupera_imagem( id )
    if arquivo != 'capa_padrao.jpg':
        os.remove( os.path.join( app.config[ 'UPLOAD_PATH' ] ), arquivo )