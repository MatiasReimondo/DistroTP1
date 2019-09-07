import connexion


def create_app():
    app = connexion.App(__name__, specification_dir='./api')
    app.add_api('swagger.yml')
    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=8080, debug=True)
