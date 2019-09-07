import json
from flask import abort, make_response
from .resolver import Resolver
from .domain import Domain

resolver = Resolver()

# GET /domains/{domain}
#Falta round robin
def obtener_dominio(domain):
    try:
        domains_answer = resolver.resolve(domain)
    except:
        return make_response({},404)
    result = json.dumps(domains_answer.__dict__)
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

    dup = resolver.search_custom_domain(domain).custom
    if dup:
        return make_response({},400)

    new_custom = resolver.save_custom_domain(domain,ip)
    response = make_response(new_custom, 201)
    response.mimetype = 'application/json'
    return response


