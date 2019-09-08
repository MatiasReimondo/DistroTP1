from dns import resolver

from api.domain import Domain


class DNSResolver:
    def resolve(self, name):
        results = []
        result = resolver.query(name)
        for answer in result.response.answer:
            results.append(self.parse_domain(name, str(answer)))
        return results

    def parse_domain(self, name, response_line):
        return Domain(name, response_line.split(" ")[4], False)
