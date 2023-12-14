from flask import Flask
from flask_smorest import Api
from resources.stores import stores_blp
from resources.items import items_blp
from db import DataBase as db

def create_app():
    app = Flask(__name__)

    app.config["API_TITLE"] = "My API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    with app.app_context():
        db.initialize_db()
    api = Api(app)
    api.register_blueprint(stores_blp)
    api.register_blueprint(items_blp)
    return app

app = create_app()
