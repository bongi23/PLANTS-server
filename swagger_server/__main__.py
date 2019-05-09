#!/usr/bin/env python3

import connexion

from swagger_server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    #app.config['MONGO_URI'] = 'mongodb://localhost:27017/plantsDB'
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'P.L.A.N.T.S. sink api'})
    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
