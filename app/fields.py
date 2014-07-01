from flask.ext.restful.fields import Integer, List, Nested, String

roll_fields = {
    'id': Integer,
    'pins': Integer
}

frame_fields = {
    'id': Integer,
    'number': Integer,
    'score': Integer,
    'rolls': List(Nested(roll_fields))
}

player_fields = {
    'id': Integer,
    'name': String,
    'frames': List(Nested(frame_fields))
}

game_fields = {
    'id': Integer,
    'players': List(Nested(player_fields))
}
