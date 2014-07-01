"""
This is a REST API to simulate a bowling algorithm.

Example::

   from requests import post, put, get, delete
   games = get('http://localhost:5000/v1/games').json()

Returns a list of games currently in the system.  For more examples and the full api, see :py:mod:`app.resources.game`

"""
from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy

__version__ = 'v1'


def create_app():
    """Creates the flask app and configures it.
    """
    app = Flask(__name__)
    app.config.from_object('config')
    return app


def get_db(app):
    """Creates the sqlalchemy database and returns it.
    """
    return SQLAlchemy(app)

app = create_app()
db = get_db(app)

from app.resources import (
    GamesResource, GameResource, RollResource)

api = restful.Api(app, prefix="/"+__version__)

api.add_resource(GamesResource, '/games')
api.add_resource(GameResource, '/games/<string:game_id>')
api.add_resource(RollResource, '/games/<string:game_id>/roll')

if __name__ == '__main__':
    app.run(debug=True)
