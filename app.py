import logging
import os
import sys

from flask import Flask, g

from internal.api.items import item_bp
from internal.db.migration.db_migration import init_db


def create_app():
    app = Flask(__name__)
    logging.basicConfig(
        stream=sys.stdout,
        format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',
        level=logging.INFO
    )
    config_path = os.environ.get('ENV_CONFIG_PATH', './config.py')
    app.config.from_pyfile(config_path)
    app.register_blueprint(item_bp, url_prefix='/api/example/')
    app.logger.info('app is ready')
    return app


app = create_app()


@app.route("/ping", methods=['GET'])
def ping():
    return 'pong'


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        if exception:
            db.rollback()
        else:
            db.commit()
        db.close()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Database Initialized.')
