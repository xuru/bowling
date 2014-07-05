from flask.ext.restful import Resource, reqparse, marshal_with
from app.models import Game
from flask import abort
import app.fields


class GamesResource(Resource):
    """Games Resource

    Defines the end points used to get or create games.
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('players', type=str, action='append', help='List of players for this game.')

    @marshal_with(app.fields.game_fields)
    def post(self):
        """
        Create a new game.  You will need to send a list of players in the data payload.

        The JSON data should look like::

            {
                'players': [
                    'player1',
                    'player2',
                ]
            }
        """
        args = self.parser.parse_args()
        if not args["players"]:
            abort(400)

        game = Game(args['players'])
        game.save()
        return game, 200

    @marshal_with(app.fields.game_fields)
    def get(self):
        """
        Get all games in the system.
        """
        return list(Game.query.all()), 200


class GameResource(Resource):
    @marshal_with(app.fields.game_fields)
    def get(self, game_id):
        """
        Get a game with the spefic id <game_id>
        """
        game = Game.query.filter_by(id=game_id).first_or_404()

        # make sure it's scored before returning it...
        game.score()
        return game

    def delete(self, game_id):
        """
        Delete a game with the spefic id <game_id>
        """
        if not game_id:
            abort(400)
        else:
            try:
                existingGame = Game.query.get(game_id)
                existingGame.delete()
                return {"message": "Game {} deleted".format(game_id)}, 202
            except Exception:
                abort(404)
        abort(404)
