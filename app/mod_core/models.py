from app import db

# Many-to-many helper tables (for public access, use models only) -----------

# modulo_usuario = db.Table(
#     'modulo_usuario',
#     db.Column(
#         'id_component',
#         db.Integer,
#         db.ForeignKey('modulo_privado.id_component')
#     ),
#     db.Column(
#         'id_usuario',
#         db.Integer,
#         db.ForeignKey('usuario.id_usuario')
#     )
# )
#
# modulo_component = db.Table(
#     'modulo_component',
#     db.Column(
#         'id_component_pai',
#         db.Integer,
#         db.ForeignKey('modulo.id_component')
#     ),
#     db.Column(
#         'id_component_filho',
#         db.Integer,
#         db.ForeignKey('component.id_component'),
#         unique=True
#     )
# )


# Models and their simple relantionships -------------------------------------


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    email = db.Column(db.String(50), unique=True)
    senha = db.Column(db.String(64))

    tipo = db.Column(db.String(30))
    __mapper_args__ = {'polymorphic_identity': __tablename__,
                       'polymorphic_on': tipo}

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha


class Administrador(Usuario):
    __tablename__ = 'administrador'
    id_usuario = db.Column(db.Integer(), db.ForeignKey("usuario.id_usuario", ondelete="CASCADE"), primary_key=True)

    client_id = db.Column(db.Integer, db.ForeignKey('client.id_client'))
    client = db.relationship("Client", uselist=False, back_populates='administrador')

    __mapper_args__ = {'polymorphic_identity': __tablename__}

    def __init__(self, nome, email, senha):
        Usuario.__init__(self, nome, email, senha)
