from flask import request, Blueprint
from flask_restplus import Resource, Namespace, fields, abort
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from app import db
from app.mod_core.models import Usuario, Local, Tag, Interacao
from app.utils import abort_if_none, fill_object, msg

# Define the blueprint: 'auth', set its url prefix: app.url/core
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')
ns = Namespace('auth', 'Operações de autenticação de usuário')


usuario_auth_m = ns.model('usuario_auth_m', {
    'email': fields.String
})


@ns.route('/login/')
class AuthController(Resource):

    @ns.expect(usuario_auth_m)
    @ns.response(200, "Token de acesso criado")
    def post(self):
        """Retorna o token de acesso do usuario"""
        email = request.json['email']

        us = Usuario.query.filter(Usuario.email == email).first()
        abort_if_none(us, 403, 'Usuario ou senha incorretos')

        token = create_access_token(identity=us.id_usuario)

        return msg(token, 'access-token')

    # @ns.response(200, "Logout feito")
    # def delete(self):
    #     pass

