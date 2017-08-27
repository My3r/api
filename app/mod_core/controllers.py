from flask import request, g, Blueprint
from flask_restplus import Resource, Namespace, fields, abort
from werkzeug.security import check_password_hash

import sys

from app import db
from app.mod_core.models import Usuario, Local, Tag, Cidade
from app.utils import abort_if_none, fill_object, msg

# Define the blueprint: 'auth', set its url prefix: app.url/core
mod_core = Blueprint('core', __name__, url_prefix='/core')
ns = Namespace('core', 'Operations related to core')

user_m = ns.model('usuario', {
    'id_usuario': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'data_nascimento': fields.Date,
    'path_foto': fields.String
})
user_m_expect = ns.model('usario', {
    'nome': fields.String,
    'email': fields.String,
    'data_nascimento': fields.Date,
    'path_foto': fields.String,
    'senha': fields.String
})

local_m = ns.model('local', {
    'id_local': fields.Integer,
    'nome': fields.String,
    'descricao': fields.String,
    'endereço': fields.String,
    'path_foto': fields.String,
    'lat': fields.Float,
    'lng': fields.Float
})
local_m_expect = ns.model('local', {
    'nome': fields.String,
    'descricao': fields.String,
    'endereço': fields.String,
    'path_foto': fields.String,
    'lat': fields.Float,
    'lng': fields.Float
})

tag_m = ns.model('tag', {
    'id_tag': fields.Integer,
    'nome': fields.String
})
tag_m_expect = ns.model('tag', {
    'nome': fields.String
})


@ns.route('/usuario/<int:id>')
@ns.response(400, 'ID não é inteiro')
@ns.response(404, 'Não encontrado')
class UsuarioController(Resource):
    @ns.marshal_with(user_m)
    @ns.response(200, 'Retorna o model usuario no corpo da resposta')
    def get(self, id):
        """Retorna um usuário pelo ID"""
        us = Usuario.query \
            .filter(Usuario.id_usuario == id) \
            .first()
        abort_if_none(us, 404, 'Não achado')
        return us

    @ns.response(200, 'Usuario atualizado')
    @ns.expect(user_m_expect)
    def put(self, id):
        """Atualiza um usuário pelo ID"""
        us = Usuario.query\
            .filter(Usuario.id_usuario == id)\
            .first()
        abort_if_none(us, 404, 'Não achado')

        fill_object(us, request.json)
        db.session.commit()

        return msg('success!')


@ns.route('/usuario/')
class UsuarioPostController(Resource):
    @ns.response(400, 'Um dos argumentos está mal formado')
    @ns.response(200, 'Retorna uma lista de usuarios com o critério passado', user_m)
    @ns.marshal_with(user_m)
    def get(self):
        """Retorna uma lista de usuários"""
        return Usuario.query.all()

    @ns.response(404, 'Erro inesperado')
    @ns.response(400, 'O modelo está mal formado')
    @ns.response(200, 'Usuario inserido')
    @ns.expect(user_m_expect)
    def post(self):
        """Cria um novo usuário"""
        us = Usuario()
        fill_object(us, request.json)
        db.session.add(us)
        try:
            db.session.commit()
        except Exception as e:
            abort(404, e.__str__())

        return msg(us.id_usuario, 'id')


@ns.route('/usuario/<int:id>/tag/')
@ns.response(400, 'ID não é inteiro')
@ns.response(404, 'Não encontrado')
class UsuarioTagController(Resource):
    @ns.marshal_with(tag_m)
    @ns.response(200, 'Lista de tags de interesse de um usuario é retornada')
    def get(self, id):
        """Retorna a lista das tags de interesse de uma pessoa pelo ID"""
        usuario = Usuario.query.filter_by(id_usuario=id).first()
        abort_if_none(usuario, 404, 'Não achado')
        return usuario.interesses


@ns.route('/usuario/<int:id_u>/tag/<int:id_t>')
@ns.response(400, 'ID não é inteiro')
@ns.response(404, 'Não encontrado')
class UsuarioTagController(Resource):
    @ns.response(200, 'Adiciona uma tag como interesse de um usuario')
    def post(self, id_u, id_t):
        """Adiciona uma tag como interesse de um usuario pelos ID's"""
        tag = Tag.query.filter_by(id_tag=id_t).first()
        abort_if_none(tag, 404, 'Não achado')
        usuario = Usuario.query.filter_by(id_usuario=id_u).first()
        abort_if_none(usuario, 404, 'Não achado')
        usuario.interesses.append(tag)
        db.session.commit()
        return msg('Sucesso!')

    @ns.response(200, 'Uma tag é removida do interesse de um usuario')
    def delete(self, id_u, id_t):
        """Remove uma tag de interesse de um usuario pelos ID's"""
        tag = Tag.query.filter_by(id_tag=id_t).first()
        abort_if_none(tag, 404, 'Não achado')
        usuario = Usuario.query.filter_by(id_usuario=id_u).first()
        abort_if_none(usuario, 404, 'Não achado')
        usuario.interesses.remove(tag)
        db.session.commit()
        return msg('Sucesso!')


@ns.route('/local/<int:id>')
@ns.response(400, 'ID não é inteiro')
@ns.response(404, 'Não encontrado')
class LocalController(Resource):
    @ns.marshal_with(local_m)
    @ns.response(200, 'Retorna o model local no corpo da resposta')
    def get(self, id):
        """Retorna um local pelo ID"""
        lc = Local.query \
            .filter(Local.id_local == id) \
            .first()
        abort_if_none(lc, 404, 'Não achado')
        return lc

    @ns.response(200, 'Local atualizado')
    @ns.expect(local_m_expect)
    def put(self, id):
        """Atualiza um local pelo ID"""
        lc = Local.query \
            .filter(Local.id_local == id) \
            .first()
        abort_if_none(lc, 404, 'Não achado')

        fill_object(lc, request.json)
        db.session.commit()

        return msg('success!')

@ns.route('/local/')
class LocalPostController(Resource):
    @ns.response(400, 'Um dos argumentos está mal formado')
    @ns.response(200, 'Retorna uma lista de locais com o critério passado', local_m)
    @ns.marshal_with(local_m)
    def get(self):
        """Retorna uma lista locais"""
        return Local.query.all()

    @ns.response(404, 'Erro inesperado')
    @ns.response(400, 'O modelo está mal formado')
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


@ns.route('/tag/<int:id>')
@ns.response(400, 'ID não é inteiro')
@ns.response(404, 'Não encontrado')
class TagController(Resource):
    @ns.marshal_with(tag_m)
    @ns.response(200, 'Retorna o model tag no corpo da resposta')
    def get(self, id):
        """Retorna uma tag pelo ID"""
        tg = Tag.query \
            .filter(Tag.id_tag == id) \
            .first()
        abort_if_none(tg, 404, 'Não achado')
        return tg

    @ns.response(200, 'Tag atualizada')
    @ns.expect(tag_m_expect)
    def put(self, id):
        """Atualiza uma tag pelo ID"""
        tg = Tag.query \
            .filter(Tag.id_tag == id) \
            .first()
        abort_if_none(tg, 404, 'Não achado')

        fill_object(tg, request.json)
        db.session.commit()

        return msg('success!')

@ns.route('/tag/')
class TagPostController(Resource):
    @ns.response(400, 'Um dos argumentos está mal formado')
    @ns.response(200, 'Retorna uma lista de locais com o critério passado', tag_m)
    @ns.marshal_with(tag_m)
    def get(self):
        """Retorna uma lista tags"""
        return Tag.query.all()

    @ns.response(404, 'Erro inesperado')
    @ns.response(400, 'O modelo está mal formado')
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

@ns.route('/cidade/<int:id>')
@ns.response(400, 'ID não é inteiro')
@ns.response(404, 'Não encontrado')
class CidadeController(Resource):
    @ns.marshal_with(local_m)
    @ns.response(200, 'Retorna uma lista de locais com o critério passado', local_m)
    def get(self, id):
        """Retorna uma lista de locais de uma cidade pelo ID"""
        ls = Local.query \
            .filter(Local.cidade_id == id) \
            .all()
        abort_if_none(ls, 404, 'Não achado')
        return ls


@ns.route('/local/<int:id>/tag/')
@ns.response(400, 'ID não é inteiro')
@ns.response(404, 'Não encontrado')
class LocalTagController(Resource):
    @ns.marshal_with(tag_m)
    @ns.response(200, 'Lista de tags de um local é retornada')
    def get(self, id):
        """Retorna a lista das tags de um local pelo ID"""
        local = Local.query.filter_by(id_local=id).first()
        abort_if_none(local, 404, 'Não achado')
        return local.tags


@ns.route('/local/<int:id_l>/tag/<int:id_t>')
@ns.response(400, 'ID não é inteiro')
@ns.response(404, 'Não encontrado')
class LocalTagController(Resource):
    @ns.response(200, 'Uma tag é adicionada a um local')
    def post(self, id_l, id_t):
        """Adiciona uma tag a um local pelos ID's"""
        tag = Tag.query.filter_by(id_tag=id_t).first()
        abort_if_none(tag, 404, 'Não achado')
        local = Local.query.filter_by(id_local=id_l).first()
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
