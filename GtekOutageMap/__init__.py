from os import environ, path, makedirs
from dotenv import load_dotenv

from flask import Flask
from flask_wtf.csrf import CSRFProtect


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    csrf = CSRFProtect(app)


    PROJECT_DIR = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(PROJECT_DIR, ".env"))

    app.config['GOOGLE_MAPS_API_KEY'] = environ.get('GOOGLE_MAPS_API_KEY', '')
    app.config['REPORT_TTL_DAYS'] = environ.get('REPORT_TTL_DAYS', 0)

    app.config.from_mapping(
        SECRET_KEY=environ.get('SECRET_KEY', 'dev'),
        DATABASE=path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    makedirs(app.instance_path, exist_ok=True)

    from . import db
    db.init_app(app)

    from . import auth, tech, outage_map, status
    app.register_blueprint(auth.bp)
    app.register_blueprint(tech.bp)
    app.register_blueprint(outage_map.bp)
    app.register_blueprint(status.bp)
    app.add_url_rule('/', endpoint='index')

    return app