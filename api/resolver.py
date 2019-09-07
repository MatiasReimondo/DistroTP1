import dns.resolver
from .domain import Domain

class Resolver:

    def resolve(self, domain):
        results = []
        result = dns.resolver.query(domain)
        print(result)
        for answer in result.response.answer:
            results.append(self.parse_domain(domain,str(answer)))
        return results

    def parse_domain(self,domain,domain_line):
        return Domain(domain,domain_line.split(' ')[4],False)

