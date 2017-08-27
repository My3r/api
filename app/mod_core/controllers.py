from flask import request, g, Blueprint
from flask_restplus import Resource, Namespace, fields, abort
from werkzeug.security import check_password_hash

import sys

from app import db
from app.mod_core.models import Usuario
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

@ns.route('/usuario/<int:id>')
@ns.response(403, 'Usuário não tem permissão')
@ns.response(400, 'ID não é inteiro')
@ns.response(404, 'Não encontrado')
class UserController(Resource):
    @ns.marshal_with(user_m)
    @ns.response(200, 'Returns the user model on the body of the response')
    def get(self, id):
        """Get an user by ID"""
        us = Usuario.query \
            .filter(Usuario.id_usuario == id) \
            .first()
        abort_if_none(us, 404, 'Não achado')
        return us

    @ns.response(200, 'Usuario atualizado')
    @ns.expect(user_m_expect)
    def put(self, id):
        """Update an user by ID"""
        us = Usuario.query\
            .filter(Usuario.id_usuario == id)\
            .first()
        abort_if_none(us, 404, 'Não achado')

        fill_object(us, request.json)
        db.session.commit()

        return msg('success!')

    @ns.response(200, 'User disabled on db')
    def delete(self, id, ):
        """Delete an user by ID"""
        us = Usuario.query.filter(Usario.id_usuario == id) \
            .first()
        abort_if_none(us, 404, 'not found')



        db.session.commit()

        return msg('disabled on db')


@ns.route('/usuario/')
@ns.response(403, 'Usuário não tem permissão')
class UserPostController(Resource):
    @ns.response(400, 'Um dos argumentos está mal formado')
    @ns.response(200, 'Retorna uma lista de usuarios com o critério passado', user_m)
    @ns.marshal_with(user_m)
    def get(self):
        """Get a list of users"""
        return Usuario.query.all()

    @ns.response(404, 'Erro inesperado')
    @ns.response(400, 'O modelo está mal formado')
    @ns.response(200, 'Usuario inserido')
    @ns.expect(user_m_expect)
    def post(self):
        """Create a new user"""
        us = Usuario()
        fill_object(us, request.json)
        db.session.add(us)
        try:
            db.session.commit()
        except Exception as e:
            abort(404, e.__str__())

        return msg(us.id_usuario, 'id')


# @ns.route('/user/resetpassword/')
# @ns.response(403, 'User is not logged, not have permission or the password is incorrect')
# @ns.response(400, 'The input is wrong')
# @ns.response(404, 'User not Found')
# @ns.response(200, 'The password is successfully altered. Obs: You need login again, to receive new token.')
# @ns.header('Authorization', 'The authorization token')
# class PasswordController(Resource):
#
#     @ns.expect(password_reset_m)
#     def put(self):
#         """Change the password"""
#         us = User.query \
#             .filter(User.disabled == 0) \
#             .filter(User.id_user == g.current_user) \
#             .first()
#         abort_if_none(us, 404, 'User not found')
#
#         if not check_password_hash(us.password, request.json['old_password']):
#             return msg('Old password incorrect'), 403
#
#         us.password = request.json['password']
#         db.session.commit()
#         cache.blacklisted_tokens.append(request.headers['Authorization'])
#
#         return msg('success!')