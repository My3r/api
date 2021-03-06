from app import db
from app.mod_core.models import Local, Tag, Cidade, Pais
import csv

locais = []
locais2 = []
locais3 = []
tmp = []
tmp2 = []
tmp3 = []

with open("Local - Natal.csv", 'r', encoding='utf-8') as f:
    records = csv.DictReader(f)
    for row in records:
         tmp.append(row)

for local in tmp:
    x = dict()
    x['cidade'] = 'Natal'
    x['nome'] = local['nome']
    x['descricao'] = local['descricao']
    x['lat'] = local['lat']
    x['lng'] = local['lng']
    x['tags'] = local['tags'].split('#')
    del(x['tags'][0])
    for i in range(0, len(x['tags'])):
        x['tags'][i] = x['tags'][i].strip().lower()
    locais.append(x)

tags = []
for local in locais:
    tags += local['tags']
tags = sorted(set(tags))


with open("Local - Mundo.csv", 'r', encoding='utf-8') as f:
    records = csv.DictReader(f)
    for row in records:
        tmp2.append(row)

for local in tmp2:
    x = dict()
    x['pais'] = local['pais']
    x['cidade'] = local['cidade']
    x['nome'] = local['nome']
    x['descricao'] = local['descricao']
    x['lat'] = local['lat']
    x['lng'] = local['lng']
    x['tags'] = local['tags'].split('#')
    del (x['tags'][0])
    for i in range(0, len(x['tags'])):
        x['tags'][i] = x['tags'][i].strip().lower()
    locais2.append(x)

for local in locais2:
    tags += local['tags']
tags = sorted(set(tags))

# print(tags)
# print(type(tags))
for tag in tags:
    t = Tag()
    t.nome = tag
    db.session.add(t)
db.session.commit()



for local in locais:
    l = Local()
    l.cidade = Cidade.query.filter_by(nome=local['cidade']).first()
    l.nome = local['nome']
    l.descricao = local['descricao']
    l.lat = (float(local['lat'].replace(',',''))/10)
    l.lng = (float(local['lng'].replace(',',''))/100)
    for tag in local['tags']:
        l.tags.append(Tag.query.filter_by(nome=tag).first())

    db.session.add(l)
db.session.commit()

pais_cidade = []

for local in locais2:
    pais_cidade.append((local['cidade'], local['pais']))

# print(pais_cidade)

for tupla in pais_cidade:
    p = Pais.query.filter_by(nome=tupla[1]).first()
    if p is None:
        p = Pais()
        p.nome = tupla[1]

    c = Cidade()
    c.nome = tupla[0]
    p.cidades.append(c)
    db.session.add(p)
db.session.commit()

for local in locais2:
    l = Local()
    l.cidade = Cidade.query.filter_by(nome=local['cidade']).first()
    l.nome = local['nome']
    l.descricao = local['descricao']
    l.lat = (float(local['lat'].replace(',', '')))
    l.lng = (float(local['lng'].replace(',', '')))
    for tag in local['tags']:
        l.tags.append(Tag.query.filter_by(nome=tag).first())

    db.session.add(l)
db.session.commit()


with open("Local - Religioso.csv", 'r', encoding='utf-8') as f:
    records = csv.DictReader(f)
    for row in records:
         tmp3.append(row)

for local in tmp3:
    x = dict()
    x['cidade'] = 'Natal'
    x['nome'] = local['nome']
    x['descricao'] = local['descricao']
    x['lat'] = local['lat']
    x['lng'] = local['lng']
    x['tags'] = local['tags'].split('#')
    del(x['tags'][0])
    for i in range(0, len(x['tags'])):
        x['tags'][i] = x['tags'][i].strip().lower()
    locais3.append(x)

for local in locais3:
    l = Local()
    l.cidade = Cidade.query.filter_by(nome=local['cidade']).first()
    l.nome = local['nome']
    l.descricao = local['descricao']
    l.lat = (float(local['lat'].replace(',',''))/10)
    l.lng = (float(local['lng'].replace(',',''))/100)
    for tag in local['tags']:
        l.tags.append(Tag.query.filter_by(nome=tag).first())

    db.session.add(l)
db.session.commit()
