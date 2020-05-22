from flask import Flask

from config import DevelopmentConfig


def create_app(config: object = None) -> object:
    app = Flask(__name__)
    with app.app_context():
        configure_app(app, config)
        configure_extensions(app)
        configure_blueprints(app)
        configure_jinja(app)
        configure_logging(app)
    return app


def configure_app(
    app: object,
    config: object = None,
) -> None:
    conf = config if config else DevelopmentConfig
    app.config.from_object(conf)


def configure_extensions(app: object) -> None:
    from app.extensions import db, migrate, login
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'default.login'


def configure_blueprints(app: object) -> None:
    from app.default.views import default_views
    from app.users.views import users_views
    for blueprint in [default_views, users_views]:
        app.register_blueprint(blueprint)


def configure_jinja(app: object) -> None:
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    # Globals
    app.jinja_env.globals['APP_NAME'] = app.config['APP_NAME']

    # Filters
    from app.common.filters import truncate
    app.jinja_env.filters['truncate'] = truncate


def configure_logging(app: object) -> None:
    if not app.debug and not app.testing:
        ''' Logging logic goes here. '''