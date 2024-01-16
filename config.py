import os

SECRET_KEY = 'casao' # senha secreta necessária.

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = 'localhost',
        database = 'jogoteca'
    ) # ORM.

UPLOAD_PATH = os.path.dirname( os.path.abspath( __file__ ) ) + '/uploads' # path dinâmico dos uploads.