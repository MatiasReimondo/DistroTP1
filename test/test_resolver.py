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


def test_round_robin():
    resolver = Resolver()
    first_answer = resolver.resolve("yahoo.com")
    second_answer = resolver.resolve("yahoo.com")

    assert first_answer.ip != second_answer.ip


def test_round_robin_loops_back():
    resolver = Resolver()
    first_ip = resolver.resolve("yahoo.com").ip
    current = None
    length = 0
    while first_ip != current:
        length += 1
        current = resolver.resolve("yahoo.com").ip

    assert length > 1


def test_cname_is_ignored():
    resolver = Resolver()
    first_answer = resolver.resolve("productforums.google.com")

    assert legal_ip_address(first_answer.ip)


def legal_ip_address(ip):
    ipv4_valid = string.digits + "."
    for char in ip:
        if char not in ipv4_valid:
            return False
    return True
