#!/usr/bin/env python3

import connexion
from flask_cors import CORS


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.add_api('swagger.yaml', arguments={'title': 'P.L.A.N.T.S. API'})
    CORS(app.app)
    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
