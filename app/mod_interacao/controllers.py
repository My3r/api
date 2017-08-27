from flask import request, Blueprint
from flask_restplus import Resource, Namespace, fields, abort

from app import db
from app.mod_core.models import Usuario, Local, Tag, Interacao
from app.utils import abort_if_none, fill_object, msg

# Define the blueprint: 'auth', set its url prefix: app.url/core
mod_interacao = Blueprint('interacao', __name__, url_prefix='/interacao')
ns = Namespace('interacao', 'Operações de interação entre usuário e local')


interacao_m = ns.model('interacao', {
    'usuario_id': fields.Integer,
    'local_id': fields.Integer,
    'like': fields.Boolean,
    'data': fields.Date
})


@ns.route('/usuario/<int:id>/interacao')
@ns.response(404, 'Não encontrado')
class InteracaoController(Resource):
    @ns.marshal_with(interacao_m)
    @ns.response(200, 'Lista de interações do usuário é retornada')
    def get(self, id):
        """Retorna a lista das interacoes de uma pessoa pelo ID"""
        interacoes = Interacao.query.filter_by(usuario_id=id).all()
        abort_if_none(interacoes, 404, 'Não achado')
        return interacoes


@ns.route('/usuario/<int:id_u>/interacao/<int:id_l>')
@ns.response(404, 'Não encontrado')
class InteracaoController(Resource):
    @ns.response(200, 'Deleta interação entre um usuário e um local')
    def delete(self, id_u, id_l):
        """Delete uma interação entre uma pessoa e um local pelos ID's"""
        interacao = Interacao.query.filter(Interacao.usuario_id==id_u).filter(Interacao.local_id).first()
        abort_if_none(interacao, 404, 'Não achado')
        db.session.delete(interacao)
        db.session.commit()
        return msg('success!')


@ns.route('/usuario/interacao')
@ns.response(404, 'Erro')
class InteracaoController(Resource):
    @ns.expect(interacao_m)
    @ns.response(200, 'Cadastra interação de um usuário com um local')
    def post(self):
        """Cria uma nova interação entre um usuário e um local"""
        i = Interacao()
        fill_object(i, request.json)
        db.session.add(i)
        try:
            db.session.commit()
        except Exception as e:
            abort(404, e.__str__())
        return msg('Sucesso!')