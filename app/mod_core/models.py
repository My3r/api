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

agenda_colaborador = db.Table('agenda_colaborador',
    db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario')),
    db.Column('id_agenda', db.Integer, db.ForeignKey('agenda.id_agenda'))
)

usuario_favorito = db.Table('usuario_favorito',
    db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario')),
    db.Column('id_local', db.Integer, db.ForeignKey('local.id_local'))
)

categoria_subcategoria = db.Table("categoria_subcategoria",
    db.Column("id_categoria", db.Integer, db.ForeignKey("categoria.id_categoria")),
    db.Column("id_subcategoria", db.Integer, db.ForeignKey("subcategoria.id_subcategoria"), unique=True)
)

# Models and their simple relantionships -------------------------------------


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    path_foto = db.Column(db.String(80))
    email = db.Column(db.String(50), unique=True)
    senha = db.Column(db.String(64))

    favoritos = db.relationship("Local",
                            secondary=usuario_favorito,
                            backref="favoritado_por")

    agendas = db.relationship("Agenda", back_populates="dono")

    agendas_colaborando = db.relationship("Agenda",
                            secondary=agenda_colaborador,
                            back_populates="colaboradores")


    tipo = db.Column(db.String(30))
    __mapper_args__ = {'polymorphic_identity': __tablename__,
                       'polymorphic_on': tipo}


class Pais(db.Model):
    __tablename__ = 'pais'
    id_pais = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    sigla = db.Column(db.String(4))

    estados = db.relationship("Estado", back_populates="pais")


class Estado(db.Model):
    __tablename__ = 'estado'
    id_estado = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    uf = db.Column(db.String(4))

    pais_id = db.Column(db.Integer, db.ForeignKey('pais.id_pais'))
    pais = db.relationship("Pais", back_populates="estados")

    cidades = db.relationship("Cidade", back_populates="estado")


class Cidade(db.Model):
    __tablename__ = 'cidade'
    id_cidade = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    sigla = db.Column(db.String(5))

    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id_estado'))
    estado = db.relationship("Estado", back_populates="cidades")

    locais = db.relationship("Local", back_populates="cidade")

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))

    locais = db.relationship("Local", back_populates="categoria")

    subcategorias = db.relationship("Subcategoria",
                                    secondary=categoria_subcategoria,
                                    backref="categoria",
                                    primaryjoin=id_categoria==categoria_subcategoria.c.id_categoria,
                                    secondaryjoin=id_categoria==categoria_subcategoria.c.id_subcategoria)

    tipo = db.Column(db.String(30))
    __mapper_args__ = {'polymorphic_identity': __tablename__,
                       'polymorphic_on': tipo}

class Subcategoria(Categoria):
    __tablename__ = 'subcategoria'
    id_subcategoria = db.Column(db.Integer, db.ForeignKey("categoria.id_categoria", ondelete="CASCADE"), primary_key=True)

    __mapper_args__ = {'polymorphic_identity': __tablename__}


class Local(db.Model):
    __tablename__ = 'local'
    id_local = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(80))
    path_foto = db.Column(db.String(80))
    descricao = db.Column(db.String(250))
    endereco = db.Column(db.String(120))
    lat = db.Column(db.Float(Precision=64))
    lng = db.Column(db.Float(Precision=64))

    agendas = db.relationship("Agenda",
                            secondary=agenda_local,
                            back_populates="locais")

    cidade_id = db.Column(db.Integer, db.ForeignKey('cidade.id_cidade'))
    cidade = db.relationship("Cidade", back_populates="locais")

    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'))
    categoria = db.relationship("Categoria", back_populates="locais")


