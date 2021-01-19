import os

from flask import Flask, render_template
from flasgger import Swagger

from .server.api.customers import customers
from .server.api.employees import employees
from .server.api.inventory import inventory
from .server.api.movies import movies
from .server.api.pos import pos
from .server.api.rentals import rentals
from .server.api.user import user


def create_app():
    app = Flask(__name__)

    app.register_blueprint(customers)
    app.register_blueprint(employees)
    app.register_blueprint(inventory)
    app.register_blueprint(movies)
    app.register_blueprint(pos)
    app.register_blueprint(rentals)
    app.register_blueprint(user)

    appTitle = 'Unbreakable API'

    app.config['SWAGGER'] = {'title': appTitle}
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json'
            }
        ],
        "swagger_ui": False
    }
    Swagger(app, config=swagger_config)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    # pylint: disable=unused-variable
    def catch_all(path):
        return appTitle

    return app
