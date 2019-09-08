from api.resolver import Resolver


def test_resolver():
    resolver = Resolver()
    answer = resolver.resolve("google.com.ar")
    assert answer.domain == 'google.com.ar'


def test_resolver_domain_is_not_custom():
    resolver = Resolver()
    answer = resolver.resolve("google.com.ar")
    assert answer.custom is False
