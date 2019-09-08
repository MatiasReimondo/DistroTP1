from api.dns_resolver import DNSResolver
from api.exceptions import DomainNotFoundError, DomainAlreadyExistsError
from .domain import Domain
import json


class Resolver:
    instance = None

    @classmethod
    def get_instance(cls):  # Singleton!
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.domains = {}
        self.dns_resolver = DNSResolver()

    def resolve(self, domain):
        try:
            domain_resolve = self._search_custom_domain(domain)
            return domain_resolve
        except DomainNotFoundError:
            return self._resolve_dns(domain)[0]

    def _resolve_dns(self, domain):
        return self.dns_resolver.resolve(domain)

    def _search_custom_domain(self, domain):
        if domain not in self.domains:
            raise DomainNotFoundError

        return Domain(domain, self.domains[domain].ip, True)

    def save_custom_domain(self, domain, ip):
        if domain in self.domains:
            raise DomainAlreadyExistsError
        new_custom = Domain(domain, ip, True)
        self.domains[domain] = new_custom
        return new_custom

    def remove_custom_domain(self, domain):
        if domain not in self.domains:
            raise DomainNotFoundError
        custom = self.domains.pop(domain)
        return custom

    def modify_custom_domain(self, domain_name, new_domain, ip):
        if domain_name not in self.domains:
            raise DomainNotFoundError

        domain = self.domains[domain_name]

        domain.domain = new_domain
        domain.ip = ip
        self.domains[new_domain] = domain
        del self.domains[domain_name]
        return domain

    def get_all_customs(self):
        result = []
        for custom_domain in self.domains.values():
            json_domain = json.loads(custom_domain)
            result.append(json_domain)
        return result

    def get_customs_filter(self, filter):
        result = []
        for custom_domain in self.domains.values():
            json_domain = json.loads(custom_domain)
            if filter in json_domain.get("domain"):
                result.append(json_domain)
        return result
