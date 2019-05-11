#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from flask import Flask
from flakon import SwaggerBlueprint
import os

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.json_encoder = encoder.JSONEncoder

    app.add_api('api.yaml', arguments={'title': 'P.L.A.N.T.S. sink api'})

    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
