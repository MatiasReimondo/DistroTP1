import json
from flask import make_response, request

from api.exceptions import DomainNotFoundError, DomainAlreadyExistsError
from .resolver import Resolver
from .custom_domains import CustomDomains

resolver = Resolver()


# GET /domains/{domain}
# Falta round robin
def obtener_dominio(domain):
    try:
        domains_answer = resolver.resolve(domain)
    except:
        return make_response({}, 404)
    result = json.dumps(domains_answer.__dict__)
    response = make_response(result, 200)
    response.mimetype = "application/json"
    return response


# GET /api/custom-domain?q=<string>
def obtener_dominios():
    param = request.args.get("q")
    if not param:
        items = resolver.get_all_customs()
    else:
        items = resolver.get_customs_filter(param)
    customs = json.dumps(CustomDomains(items).__dict__)
    response = make_response(customs, 200)
    response.mimetype = "application/json"
    return response


# POST /api/custom-domains
def agregar_dominio(**kwargs):
    custom = kwargs.get("body")
    domain = custom.get("domain")
    ip = custom.get("ip")
    if not domain or not ip:
        return make_response({}, 400)

    try:
        new_custom = resolver.save_custom_domain(domain, ip)
    except DomainAlreadyExistsError:
        return make_response({}, 400)

    response = make_response(new_custom, 201)
    response.mimetype = "application/json"
    return response


# PUT /api/custom-domains/{domain}
def modificar_dominio(domain, **kwargs):
    custom = kwargs.get("body")
    domain_body = custom.get("domain")
    ip = custom.get("ip")

    if not domain_body or not ip or domain != domain_body:
        return make_response({}, 400)

    try:
        custom_domain = resolver.modify_custom_domain(domain_body, ip)
    except DomainNotFoundError:
        return make_response({}, 404)

    response = make_response(custom_domain, 200)
    response.mimetype = "application/json"
    return response


# DELETE /api/custom-domains/{domain}
def eliminar_dominio(domain):
    try:
        resolver.remove_custom_domain(domain)
    except DomainNotFoundError:
        return make_response({}, 404)

    result = {"domain": domain}
    response = make_response(result, 200)
    response.mimetype = "application/json"
    return response
