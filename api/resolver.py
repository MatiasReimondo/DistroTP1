from api.dns_resolver import DNSResolver
from api.exceptions import DomainNotFoundError, DomainAlreadyExistsError
from .domain import Domain


class Resolver:
    instance = None

    @classmethod
    def get_instance(cls):  # Singleton!
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.custom_domains = {}
        self.domains = {}
        self.dns_resolver = DNSResolver()

    def resolve(self, domain):
        try:
            return self._search_custom_domain(domain)
        except DomainNotFoundError:
            return self._search_non_custom_domain(domain)

    def _search_non_custom_domain(self, domain):
        if domain not in self.domains:
            domain_info = self._fetch_from_dns(domain)
            self.domains[domain] = domain_info

        return self._domain_from_round_robin(domain)

    def _fetch_from_dns(self, domain):
        domains = self.dns_resolver.resolve(domain)
        return {"domains": domains, "current": 0}

    def _search_custom_domain(self, domain):
        if domain not in self.custom_domains:
            raise DomainNotFoundError

        return Domain(domain, self.custom_domains[domain].ip, True)

    def save_custom_domain(self, domain, ip):
        if domain in self.custom_domains:
            raise DomainAlreadyExistsError
        new_custom = Domain(domain, ip, True)
        self.custom_domains[domain] = new_custom
        return new_custom

    def remove_custom_domain(self, domain):
        if domain not in self.custom_domains:
            raise DomainNotFoundError
        custom = self.custom_domains.pop(domain)
        return custom

    def modify_custom_domain(self, domain_name, new_domain, ip):
        if domain_name not in self.custom_domains:
            raise DomainNotFoundError

        domain = self.custom_domains[domain_name]
        domain.ip = ip
        return domain

    def get_all_customs(self):
        result = []
        for custom_domain in self.custom_domains.values():
            json_domain = custom_domain.__dict__
            result.append(json_domain)
        return result

    def get_customs_filter(self, filter_term):
        result = self.get_all_customs()
        return [x for x in result if filter_term in x["domain"]]

    def _domain_from_round_robin(self, domain):
        domain_info = self.domains[domain]
        result = domain_info["domains"][domain_info["current"]]
        domain_info["current"] = (domain_info["current"] + 1) % len(
            domain_info["domains"]
        )
        return result
