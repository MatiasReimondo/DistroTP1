import json
from flask import abort, make_response
from .resolver import Resolver
from .domain import Domain

# Data to serve with our API
domains= {}


# GET /domains/{domain}
#Falta round robin
def obtener_dominio(domain):
    resolver = Resolver()
    try:
        domains_answer = resolver.resolve(domain)
    except:
        return make_response({},404)
    result = json.dumps(domains_answer[0].__dict__)
    response = make_response(result, 200)
    response.mimetype = 'application/json'
    return response

# POST /api/custom-domain
def agregar_dominio(**kwargs):
    custom = kwargs.get('body')
    domain = custom.get('domain')
    ip = custom.get('ip')
    if not domain or not ip:
        return make_response({},400)

    dup = False
    for dominio_existente in domains.values():
        dup = domain == json.loads(dominio_existente).get('domain')
        if dup: break
    if dup:
        return make_response({},400)

    new_custom = json.dumps(Domain(domain,ip,True).__dict__)
    domains[domain] = new_custom
    response = make_response(new_custom, 201)
    response.mimetype = 'application/json'
    return response

