import json
from flask import make_response, request

from api.exceptions import DomainNotFoundError, DomainAlreadyExistsError
from .resolver import Resolver
from .custom_domains import CustomDomains
from .error import Error

resolver = Resolver.get_instance()

DOMAIN_NOT_FOUND = "domain not found"
BAD_DOMAIN = "custom domain already exists"
INVALID_PAYLOAD = "payload is invalid"

# GET /domains/{domain}
def obtener_dominio(domain):
    try:
        domains_answer = resolver.resolve(domain)
    except:
        return respuesta_error(404, DOMAIN_NOT_FOUND)
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
        return respuesta_error(400, BAD_DOMAIN)

    try:
        new_custom = resolver.save_custom_domain(domain, ip)
    except DomainAlreadyExistsError:
        return respuesta_error(400, BAD_DOMAIN)

    response = make_response(json.dumps(new_custom.__dict__), 201)
    response.mimetype = "application/json"
    return response


# PUT /api/custom-domains/{domain}
def modificar_dominio(domain, **kwargs):
    custom = kwargs.get("body")
    domain_body = custom.get("domain")
    ip = custom.get("ip")

    if not domain_body or not ip or domain_body != domain:
        return respuesta_error(400, INVALID_PAYLOAD)

    try:
        custom_domain = resolver.modify_custom_domain(domain, domain_body, ip)
    except DomainNotFoundError:
        return respuesta_error(404, DOMAIN_NOT_FOUND)

    response = make_response(json.dumps(custom_domain.__dict__), 200)
    response.mimetype = "application/json"
    return response


# DELETE /api/custom-domains/{domain}
def eliminar_dominio(domain):
    try:
        resolver.remove_custom_domain(domain)
    except DomainNotFoundError:
        return respuesta_error(404, DOMAIN_NOT_FOUND)

    result = {"domain": domain}
    response = make_response(result, 200)
    response.mimetype = "application/json"
    return response


def respuesta_error(codigo, mensaje):
    error = json.dumps(Error(mensaje).__dict__)
    response = make_response(error, codigo)
    response.mimetype = "application/json"
    return response
