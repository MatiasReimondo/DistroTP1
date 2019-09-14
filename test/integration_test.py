import csv

import requests


def integration_test():
    """
    Precondición: bajarse el archivo de dominios
    https://www.domcop.com/top-10-million-domains
    Y tenerlo en el root del repo como top10milliondomains.csv

    Luego, levantar la API en el port 8080
    """
    with open('top10milliondomains.csv') as domains:
        reader = csv.DictReader(domains)
        for row in reader:
            _read_row(row)


def _read_row(row):
    domain = row['Domain']
    response = requests.get(f'http://localhost:8080/api/domains/{row["Domain"]}')
    body = response.json()
    if response.status_code != 200:
        print(f'{domain} devolvió error: {body["error"]}')
    else:
        print(f'{domain} tiene IP: {body["ip"]}')


if __name__ == '__main__':
    integration_test()
