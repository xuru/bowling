from flask.ext.restful import Resource, reqparse, marshal_with
from flask import abort
import app.fields
from app.models import Player


class RollResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('pins', type=int, help='Number of pins for this roll')
        self.parser.add_argument('player_id', type=int, help='Player id of the specific game')

    @marshal_with(app.fields.roll_fields)
    def put(self, game_id):
        args = self.parser.parse_args()
        pins = int(args['pins'])
        player_id = args['player_id']

        player = Player.query.get(player_id)
        if not player:
            abort(404, message="Player {} doesn't exist".format(player_id))

        roll = player.roll(pins)
        if not roll:
            abort(404, message="Player {} doesn't have any more rolls".format(player_id))

        return roll, 200
