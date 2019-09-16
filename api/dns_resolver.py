from dns import resolver

from api.domain import Domain


class DNSResolver:
    def resolve(self, name):
        results = []
        result = resolver.query(name)
        for answer in result.response.answer:
            results.append(self.parse_domain(name, str(answer)))

        result_flat = []
        [result_flat.extend(result) for result in results]
        return result_flat

    def parse_domain(self, name, response_line):
        lines = response_line.split("\n")
        lines = [line for line in lines if 'CNAME' not in line]
        return [Domain(name, line.split(" ")[4], False) for line in lines]
