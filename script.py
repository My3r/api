from app.mod_core.models import *
from app import db

rodrigo = Usuario()
rodrigo.nome = 'Rodrigo Castro'
rodrigo.email = 'rodrigondec@gmail.com'
rodrigo.senha = 'rodrigo123'
rodrigo.data_nascimento = '1994-12-27'
rodrigo.path_foto = '~/r.png'

db.session.add(rodrigo)
db.session.commit()

brasil = Pais()
brasil.nome = 'Brasil'
brasil.sigla = 'BR'
db.session.add(brasil)

rn = Estado()
rn.nome = 'Rio Grande do Norte'
rn.uf = 'RN'

brasil.estados.append(rn)

natal = Cidade()
natal.nome = 'Natal'
natal.sigla = 'NAT'
rn.cidades.append(natal)

db.session.commit()
