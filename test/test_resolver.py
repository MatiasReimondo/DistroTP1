import string

from api.resolver import Resolver


def test_resolver():
    resolver = Resolver()
    answer = resolver.resolve("google.com.ar")
    assert answer.domain == "google.com.ar"


def test_resolver_domain_is_not_custom():
    resolver = Resolver()
    answer = resolver.resolve("google.com.ar")
    assert answer.custom is False


def test_domain_parsing_returns_an_ip():
    resolver = Resolver()
    answer = resolver.resolve("yahoo.com")
    assert legal_ip_address(answer.ip)


def legal_ip_address(ip):
    ipv4_valid = string.digits + '.'
    for char in ip:
        if char not in ipv4_valid:
            return False
    return True
