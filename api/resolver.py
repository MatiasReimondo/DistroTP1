import dns.resolver
from .domain import Domain
import json

class Resolver:
    def __init__(self):
        self.domains = {}


    def resolve(self, domain):
        domain_resolve = self.search_custom_domain(domain)
        if domain_resolve.custom:
            return domain_resolve
        domain_answer= self.resolve_dns(domain)[0]
        return domain_answer

    def resolve_dns(self, domain):
        results = []
        result = dns.resolver.query(domain)
        for answer in result.response.answer:
            results.append(self.parse_domain(domain,str(answer)))
        return results

    def parse_domain(self,domain,domain_line):
        return Domain(domain,domain_line.split(' ')[4],False)

    def search_custom_domain(self,domain):
        found = False
        for custom_domain in self.domains.values():
            json_domain = json.loads(custom_domain)
            found = domain == json_domain.get('domain')
            if found:
                return Domain(domain,json_domain.get('ip'),True)
        return Domain('','',False)

    def save_custom_domain(self,domain, ip):
        new_custom = json.dumps(Domain(domain,ip,True).__dict__)
        self.domains[domain] = new_custom
        return new_custom





