import os

from flask import Flask
from flasgger import Swagger

from .api.customers import customers
from .api.employees import employees
from .api.inventory import inventory
from .api.movies import movies
from .api.pos import pos
from .api.rentals import rentals
from .api.user import user


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
