from flask import request, Blueprint
from flask_restplus import Resource, Namespace, fields, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.mod_core.models import Usuario, Local, Tag, Interacao
from app.utils import abort_if_none, fill_object, msg

# Define the blueprint: 'auth', set its url prefix: app.url/core
mod_core = Blueprint('core', __name__, url_prefix='/core')
ns = Namespace('core', 'Operações core. CRUD de Usuario, Local e Tag')

usuario_m = ns.model('usuario_m', {
    'id_usuario': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'data_nascimento': fields.Date,
    'path_foto': fields.String
})
usuario_m_expect = ns.model('usuario_m_expect', {
    'nome': fields.String,
    'email': fields.String,
    'data_nascimento': fields.Date,
    'path_foto': fields.String,
    'senha': fields.String
})

local_m = ns.model('local_m', {
    'id_local': fields.Integer,
    'nome': fields.String,
    'descricao': fields.String,
    'endereço': fields.String,
    'path_foto': fields.String,
    'lat': fields.Float,
    'lng': fields.Float,
    'instagram_1': fields.String,
    'instagram_2': fields.String,
    'instagram_3': fields.String
})
local_m_expect = ns.model('local_m_expect', {
    'nome': fields.String,
    'descricao': fields.String,
    'endereço': fields.String,
    'path_foto': fields.String,
    'lat': fields.Float,
    'lng': fields.Float,
    'instagram_1': fields.String,
    'instagram_2': fields.String,
    'instagram_3': fields.String
})

tag_m = ns.model('tag_m', {
    'id_tag': fields.Integer,
    'nome': fields.String
})
tag_m_expect = ns.model('tag_m_expect', {
    'nome': fields.String
})


@ns.route('/usuario')
@ns.response(404, 'Não encontrado')
class UsuarioController(Resource):
    @ns.header('Authorization', 'The authorization token')
    @ns.response(200, 'Retorna o model usuario no corpo da resposta', usuario_m)
    @ns.marshal_with(usuario_m)
    @jwt_required
    def get(self):
        """Retorna um usuário pelo ID"""
        us = Usuario.query \
            .filter(Usuario.id_usuario == get_jwt_identity()) \
            .first()
        abort_if_none(us, 404, 'Não achado')
        return us

    @ns.header('Authorization', 'The authorization token')
    @ns.response(200, 'Usuario atualizado')
    @ns.expect(usuario_m_expect)
    @jwt_required
    def put(self):
        """Atualiza um usuário pelo ID"""
        us = Usuario.query\
            .filter(Usuario.id_usuario == get_jwt_identity())\
            .first()
        abort_if_none(us, 404, 'Não achado')

        fill_object(us, request.json)
        db.session.commit()

        return msg('success!')

    @ns.response(404, 'Erro inesperado')
    @ns.response(400, 'O modelo está mal formado')
    @ns.response(200, 'Usuario inserido')
    @ns.expect(usuario_m_expect)
    def post(self):
        """Cria um novo usuário"""
        us = Usuario()
        # request = request
        json = request.json
        fill_object(us, json)
        db.session.add(us)
        try:
            db.session.commit()
        except Exception as e:
            abort(404, e.__str__())

        return msg(us.id_usuario, 'id')


# @ns.route('/usuarios')
# @ns.response(404, 'Erro')
# @ns.header('Authorization', 'The authorization token')
# class UsuarioPostController(Resource):
#     @ns.response(400, 'Um dos argumentos está mal formado')
#     @ns.response(200, 'Retorna uma lista de usuarios com o critério passado', usuario_m)
#     @ns.marshal_with(usuario_m)
#     @jwt_required
#     def get(self):
#         """Retorna uma lista de usuários"""
#         return Usuario.query.all()



@ns.route('/local/<int:id_local>')
@ns.param('id_local', 'ID do local')
@ns.response(404, 'Não encontrado')
class LocalController(Resource):
    @ns.response(200, 'Retorna o model local no corpo da resposta')
    @ns.marshal_with(local_m)
    def get(self, id_local):
        """Retorna um local pelo ID"""
        lc = Local.query \
            .filter(Local.id_local == id_local) \
            .first()
        abort_if_none(lc, 404, 'Não achado')
        return lc

    @ns.response(200, 'Local atualizado')
    @ns.expect(local_m_expect)
    def put(self, id_local):
        """Atualiza um local pelo ID"""
        lc = Local.query \
            .filter(Local.id_local == id_local) \
            .first()
        abort_if_none(lc, 404, 'Não achado')

        fill_object(lc, request.json)
        db.session.commit()

        return msg('success!')

    @ns.response(200, 'Local deletado')
    def delete(self, id_local):
        """Delete um local ID's"""
        lc = Local.query \
            .filter(Local.id_local == id_local) \
            .first()
        abort_if_none(lc, 404, 'Não achado')
        db.session.delete(lc)
        db.session.commit()
        return msg('success!')


@ns.route('/local')
class LocalPostController(Resource):
    @ns.response(200, 'Retorna uma lista de locais com o critério passado', local_m)
    @ns.marshal_with(local_m)
    def get(self):
        """Retorna uma lista de locais"""
        return Local.query.all()

    @ns.response(404, 'Erro')
    @ns.response(200, 'Local inserido')
    @ns.expect(local_m_expect)
    def post(self):
        """Cria um novo local"""
        lc = Local()
        fill_object(lc, request.json)
        db.session.add(lc)
        try:
            db.session.commit()
        except Exception as e:
            abort(404, e.__str__())

        return msg(lc.id_local, 'id')


@ns.route('/tag/<int:id_tag>')
@ns.param('id_tag', 'ID da tag')
@ns.response(404, 'Não encontrado')
class TagController(Resource):
    @ns.marshal_with(tag_m)
    @ns.response(200, 'Retorna o model tag no corpo da resposta')
    def get(self, id_tag):
        """Retorna uma tag pelo ID"""
        tg = Tag.query \
            .filter(Tag.id_tag == id_tag) \
            .first()
        abort_if_none(tg, 404, 'Não achado')
        return tg

    @ns.response(200, 'Tag atualizada')
    @ns.expect(tag_m_expect)
    def put(self, id_tag):
        """Atualiza uma tag pelo ID"""
        tg = Tag.query \
            .filter(Tag.id_tag == id_tag) \
            .first()
        abort_if_none(tg, 404, 'Não achado')

        fill_object(tg, request.json)
        db.session.commit()

        return msg('success!')


@ns.route('/tag')
class TagPostController(Resource):
    @ns.response(200, 'Retorna uma lista de locais com o critério passado', tag_m)
    @ns.marshal_with(tag_m)
    def get(self):
        """Retorna uma lista tags"""
        return Tag.query.all()

    @ns.response(404, 'Erro inesperado')
    @ns.response(200, 'Tag inserido')
    @ns.expect(tag_m_expect)
    def post(self):
        """Cria uma novo tag"""
        tg = Tag()
        fill_object(tg, request.json)
        db.session.add(tg)
        try:
            db.session.commit()
        except Exception as e:
            abort(404, e.__str__())

        return msg(tg.id_tag, 'id')


@ns.route('/usuario/<int:id_usuario>/limpar')
@ns.param('id_usuario', 'ID do usuario')
@ns.response(404, 'Não encontrado')
@ns.header('Authorization', 'The authorization token')
class LimparUsuarioController(Resource):
    @ns.response(200, 'Usuario resetado')
    @jwt_required
    def delete(self, id_usuario):
        """Limpa lista de interesses e interações do usuario pelo ID"""
        us = Usuario.query \
            .filter(Usuario.id_usuario == id_usuario) \
            .first()
        abort_if_none(us, 404, 'Não achado')
        for interesse in us.interesses:
            db.session.delete(interesse)
        for interacao in us.interacoes:
            db.session.delete(interacao)
        db.session.commit()
        return msg('success!')