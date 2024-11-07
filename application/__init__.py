from flask import Flask
from application.models import db
from application.extensions import ma, limiter, cache
from application.blueprints.members import members_bp
from application.blueprints.loans import loans_bp
from application.blueprints.books import books_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs' #This will be our url endpoint to access our docs
API_URL = '/static/swagger.yaml' #Grabbing our host URL from our yaml file

swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'Library API'})


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    #Add extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)



    #register blueprints
    app.register_blueprint(members_bp, url_prefix="/members")
    app.register_blueprint(loans_bp, url_prefix="/loans")
    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)


    return app