from jogoteca import db

class Jogos( db.Model ): # classe que usa o SQLAlchemy (ORM) para representar os Jogos.
    id = db.Column( db.Integer, primary_key = True, autoincrement = True ) # chave primária e que se autoincrementa sozinho.
    nome = db.Column( db.String( 50 ), nullable = False ) # não aceita missing.
    categoria = db.Column( db.String( 40 ), nullable = False ) # não aceita missing.
    console = db.Column( db.String( 20 ), nullable = False ) # não aceita missing.

    def __repr__( self ):
        return '<Name %r>' % self.name # representação da classe.
 

class Usuarios( db.Model ): # classe que usa o SQLAlchemy (ORM) para representar os Usuários.
    nickname = db.Column( db.String( 8 ), primary_key = True ) # chave primária.
    nome = db.Column( db.String( 20 ), nullable = False ) # não aceita missing.
    senha = db.Column( db.String( 100 ), nullable = False ) # não aceita missing.

    def __repr__( self ):
        return '<Name %r>' % self.name # representação da classe.