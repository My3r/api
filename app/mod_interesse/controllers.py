from flask import request, Blueprint
from flask_restplus import Resource, Namespace, fields, abort

from app import db
from app.mod_core.models import Usuario, Local, Tag, Interacao
from app.utils import abort_if_none, fill_object, msg

# Define the blueprint: 'auth', set its url prefix: app.url/core
mod_interesse = Blueprint('interesse', __name__, url_prefix='/interesse')
ns = Namespace('interesse', 'Operações de tags interesse do usuário')


tag_m = ns.model('tag', {
    'id_tag': fields.Integer,
    'nome': fields.String
})


@ns.route('/usuario/<int:id>/tag/')
class UsuarioTagController(Resource):
    @ns.marshal_with(tag_m)
    @ns.response(200, 'Lista de tags de interesse de um usuario é retornada')
    def get(self, id):
        """Retorna a lista das tags de interesse de uma pessoa pelo ID"""
        usuario = Usuario.query.filter_by(id_usuario=id).first()
        abort_if_none(usuario, 404, 'Não achado')
        return usuario.interesses


@ns.route('/usuario/<int:id_u>/tag/<int:id_t>')
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
