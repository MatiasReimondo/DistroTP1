import json
from flask import abort, make_response
from .resolver import Resolver
from .domain import Domain


# GET /domains/{domain}
def obtener_dominio(domain):
    resolver = Resolver()
    domains_answer = resolver.resolve(domain)
    result = json.dumps(domains_answer[0].__dict__)
    response = make_response(result, 200)
    response.mimetype = 'application/json'
    return response
