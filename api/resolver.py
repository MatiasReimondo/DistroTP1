import dns.resolver

from api.exceptions import DomainNotFoundError, DomainAlreadyExistsError
from .domain import Domain
import json


class Resolver:
    def __init__(self):
        self.domains = {}

    def resolve(self, domain):
        try:
            domain_resolve = self.search_custom_domain(domain)
            return domain_resolve
        except DomainNotFoundError:
            return self.resolve_dns(domain)[0]

    def resolve_dns(self, domain):
        results = []
        result = dns.resolver.query(domain)
        for answer in result.response.answer:
            results.append(self.parse_domain(domain, str(answer)))
        return results

    def parse_domain(self, domain, domain_line):
        return Domain(domain, domain_line.split(" ")[4], False)

    def search_custom_domain(self, domain):
        found = False
        for custom_domain in self.domains.values():
            json_domain = json.loads(custom_domain)
            found = domain == json_domain.get("domain")
            if found:
                return Domain(domain, json_domain.get("ip"), True)
        raise DomainNotFoundError

    def save_custom_domain(self, domain, ip):
        if domain in self.domains:
            raise DomainAlreadyExistsError
        new_custom = json.dumps(Domain(domain, ip, True).__dict__)
        self.domains[domain] = new_custom
        return new_custom

    def remove_custom_domain(self, domain):
        if domain not in self.domains:
            raise DomainNotFoundError
        custom = self.domains.pop(domain)
        return custom

    def modify_custom_domain(self, domain_name, ip):
        if domain_name not in self.domains:
            raise DomainNotFoundError

        domain = self.domains[domain_name]

        domain.domain = domain_name
        domain.ip = ip
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
