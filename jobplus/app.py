from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from jobplus.config import configs
from jobplus.models import db, User
from jobplus.handlers import blueprints

def register_extension(app):
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)
    login_manager.login_view = 'front.login'


def register_blueprints(app: Flask):
    for bp in blueprints:
        app.register_blueprint(bp)


def register_error_handler(app: Flask):

    @app.errorhandler(404)
    def not_found(error):
        return render_template('error/404.html', 404)

    @app.errorhandler(500)
    def server_error(error):
        return render_template('error/500.html', 500)

def create_app(config):
    app = Flask(__name__)

    if isinstance(config, dict):
        app.config.update(config)
    else:
        app.config.from_object(configs.get(config, None))

    register_extension(app)
    register_blueprints(app)
    register_error_handler(app)
    return app

