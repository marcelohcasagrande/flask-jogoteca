from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask( __name__ ) # Abrindo aplicação.
app.config.from_pyfile( 'config.py' ) # Lendo as configurações do config.py.

db = SQLAlchemy( app ) # ORM.
csrf = CSRFProtect( app ) # proteção atrelada ao armazenamento de cookies. Necessário para não resultar em erros.
bcrypt = Bcrypt( app ) # para hashear senhas.

from views_game import *
from views_user import *

if __name__ == '__main__':
    app.run( debug = True )