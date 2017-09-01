from flask import Blueprint
from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import jwt_required

from app import db
from app.mod_core.models import Usuario, Tag
from app.utils import abort_if_none, msg

# Define the blueprint: 'auth', set its url prefix: app.url/core
mod_interesse = Blueprint('interesse', __name__, url_prefix='/interesse')
ns = Namespace('interesse', 'Operações de tags interesse do usuário')


tag_m = ns.model('tag_m', {
    'id_tag': fields.Integer,
    'nome': fields.String
})


@ns.route('/<int:id_usuario>')
@ns.param('id_usuario', 'ID do usuario')
@ns.header('Authorization', 'The authorization token')
class UsuarioTagController(Resource):
    @ns.marshal_with(tag_m)
    @ns.response(200, 'Lista de tags de interesse de um usuario é retornada')
    @jwt_required
    def get(self, id_usuario):
        """Retorna a lista das tags de interesse de uma pessoa pelo ID"""
        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
        abort_if_none(usuario, 404, 'Não achado')
        return usuario.interesses


@ns.route('/<int:id_usuario>/tag/<int:id_tag>')
@ns.param('id_usuario', 'ID do usuario')
@ns.param('id_tag', 'ID da tag')
@ns.header('Authorization', 'The authorization token')
class UsuarioTagController(Resource):
    @ns.response(200, 'Adiciona uma tag como interesse de um usuario')
    @jwt_required
    def post(self, id_usuario, id_tag):
        """Adiciona uma tag como interesse de um usuario pelos ID's"""
        tag = Tag.query.filter_by(id_tag=id_tag).first()
        abort_if_none(tag, 404, 'Não achado')
        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
        abort_if_none(usuario, 404, 'Não achado')
        usuario.interesses.append(tag)
        db.session.commit()
        return msg('Sucesso!')

    @ns.response(200, 'Uma tag é removida do interesse de um usuario')
    @jwt_required
    def delete(self, id_usuario, id_tag):
        """Remove uma tag de interesse de um usuario pelos ID's"""
        tag = Tag.query.filter_by(id_tag=id_tag).first()
        abort_if_none(tag, 404, 'Não achado')
        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
        abort_if_none(usuario, 404, 'Não achado')
        usuario.interesses.remove(tag)
        db.session.commit()
        return msg('Sucesso!')
