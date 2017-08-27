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

usuario_tag = db.Table('usuario_tag',
    db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario')),
    db.Column('id_tag', db.Integer, db.ForeignKey('tag.id_tag'))
)

local_tag = db.Table('local_tag',
    db.Column('id_local', db.Integer, db.ForeignKey('local.id_local')),
    db.Column('id_tag', db.Integer, db.ForeignKey('tag.id_tag'))
)

agenda_local = db.Table("agenda_local",
    db.Column("id_agenda", db.Integer, db.ForeignKey("agenda.id_agenda")),
    db.Column("id_local", db.Integer, db.ForeignKey("local.id_local"))
)

# Models and their simple relantionships -------------------------------------


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    data_nascimento = db.Column(db.Date)
    path_foto = db.Column(db.String(80))
    email = db.Column(db.String(50), unique=True)
    oauth_instagram = db.Column(db.String(80))

    favoritos = db.relationship("Local",
                            secondary=usuario_favorito,
                            backref="favoritado_por")

    interesses = db.relationship("Tag",
                             secondary=usuario_tag,
                             backref='interessados')

    agendas = db.relationship("Agenda", back_populates="dono")

    agendas_colaborando = db.relationship("Agenda",
                            secondary=agenda_colaborador,
                            back_populates="colaboradores")


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


class Tag(db.Model):
    __tablename__ = 'tag'
    id_tag = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(35))


class Local(db.Model):
    __tablename__ = 'local'
    id_local = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(80))
    path_foto = db.Column(db.String(80))
    descricao = db.Column(db.String(300))
    endereco = db.Column(db.String(120))
    lat = db.Column(db.Float(Precision=64))
    lng = db.Column(db.Float(Precision=64))

    agendas = db.relationship("Agenda",
                            secondary=agenda_local,
                            back_populates="locais")

    cidade_id = db.Column(db.Integer, db.ForeignKey('cidade.id_cidade'))
    cidade = db.relationship("Cidade", back_populates="locais")

    tags = db.relationship("Tag",
                            secondary="local_tag",
                            backref="locais")


class Agenda(db.Model):
    __tablename__ = 'agenda'
    id_agenda = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(80))

    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)

    locais = db.relationship("Local",
                            secondary=agenda_local,
                            back_populates="agendas")

    dono_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    dono = db.relationship("Usuario", back_populates="agendas")

    colaboradores = db.relationship("Usuario",
                            secondary=agenda_colaborador,
                            back_populates="agendas_colaborando")
