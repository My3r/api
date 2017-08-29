from flask import Blueprint
from flask_restplus import Resource, Namespace, fields

from app import db
from app.mod_core.models import Usuario, Local, Tag, Cidade
from app.utils import abort_if_none, msg

# Define the blueprint: 'auth', set its url prefix: app.url/core
mod_local = Blueprint('local', __name__, url_prefix='/local')
ns = Namespace('local', 'Operações de local e processamento')


local_m_t = ns.model('local', {
    'id_local': fields.Integer,
    'nome': fields.String,
    'descricao': fields.String,
    'endereço': fields.String,
    'path_foto': fields.String,
    'lat': fields.Float,
    'lng': fields.Float,
    'instagram_1': fields.String,
    'instagram_2': fields.String,
    'instagram_3': fields.String,
    'tags': fields.List(fields.String)
})

tag_m = ns.model('tag', {
    'id_tag': fields.Integer,
    'nome': fields.String
})


@ns.route('/cidade/<int:id_cidade>')
@ns.response(404, 'Não encontrado')
class CidadeController(Resource):
    @ns.marshal_with(local_m_t)
    @ns.response(200, 'Retorna uma lista de locais com o critério passado', local_m_t)
    def get(self, id_cidade):
        """Retorna uma lista de locais de uma cidade pelo ID"""
        ls = Local.query \
            .filter(Local.cidade_id == id_cidade) \
            .all()
        abort_if_none(ls, 404, 'Não achado')
        return ls


@ns.route('/<int:id_local>')
@ns.response(404, 'Não encontrado')
class LocalTagController(Resource):
    @ns.marshal_with(tag_m)
    @ns.response(200, 'Lista de tags de um local é retornada')
    def get(self, id_local):
        """Retorna a lista das tags de um local pelo ID"""
        local = Local.query.filter_by(id_local=id_local).first()
        abort_if_none(local, 404, 'Não achado')
        return local.tags


@ns.route('/<int:id_local>/tag/<int:id_tag>')
@ns.response(404, 'Não encontrado')
class LocalTagController(Resource):
    @ns.response(200, 'Uma tag é adicionada a um local')
    def post(self, id_local, id_tag):
        """Adiciona uma tag a um local pelos ID's"""
        tag = Tag.query.filter_by(id_tag=id_tag).first()
        abort_if_none(tag, 404, 'Não achado')
        local = Local.query.filter_by(id_local=id_local).first()
        abort_if_none(local, 404, 'Não achado')
        local.tags.append(tag)
        db.session.commit()
        return msg('Sucesso!')


    @ns.response(200, 'Uma tag é removida de um local')
    def delete(self, id_l, id_t):
        """Remove uma tag de um local pelos ID's"""
        tag = Tag.query.filter_by(id_tag=id_t).first()
        abort_if_none(tag, 404, 'Não achado')
        local = Local.query.filter_by(id_local=id_l).first()
        abort_if_none(local, 404, 'Não achado')
        local.tags.remove(tag)
        db.session.commit()
        return msg('Sucesso!')


@ns.route('/cidade/<int:id_cidade>/usuario/<int:id_usuario>')
@ns.response(404, 'Não encontrado')
class LocalInteresseController(Resource):
    @ns.marshal_with(local_m_t)
    @ns.response(200, 'Lista de locais ordenado decrescente por interesse do usuário')
    def get(self, id_cidade, id_usuario):
        """Retorna lista de locais ordenado por quantidade de tags de interesse do usuário"""
        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
        abort_if_none(usuario, 404, 'Não achado')
        cidade = Cidade.query.filter_by(id_cidade=id_cidade).first()
        abort_if_none(cidade, 404, 'Não achado')

        locais_interacoes = []
        for interacao in usuario.interacoes:
            locais_interacoes.append(Local.query.filter_by(id_local=interacao.local_id).first())

        locais_disponiveis = [local for local in cidade.locais if local not in locais_interacoes]

        tags_complementares = []
        for i in range(0, len(locais_disponiveis)):
            tags_complementares.append([tag for tag in locais_disponiveis[i].tags if tag not in usuario.interesses])
            # print(locais_disponiveis[i])

        for i in range(0, len(locais_disponiveis)):
            locais_disponiveis[i].tags = [tag for tag in locais_disponiveis[i].tags if tag not in tags_complementares[i]]

        locais_disponiveis = sorted(locais_disponiveis, key=lambda local: len(local.tags), reverse=True)

        return locais_disponiveis

