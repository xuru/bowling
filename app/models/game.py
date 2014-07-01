from app import db
from app.errors import APISyntaxError
from app.models.player import Player


class Game(db.Model):
    """
    Container that holds the games players (along with those players frames and rolls)
    """
    id = db.Column(db.Integer, primary_key=True)
    players = db.relationship(
        'Player', backref=db.backref('game', lazy='joined'), lazy='dynamic')

    def __init__(self, players=None):
        if players:
            if isinstance(players, str):
                self.players.append(Player(self, players))
            elif isinstance(players, (list, tuple)):
                for player in players:
                    if isinstance(player, str):
                        self.players.append(Player(self, player))
                    else:
                        raise APISyntaxError("Players has unknown objects of type {}".format(type(player)))
        else:
            raise APISyntaxError("Players are required to create a game.")
        db.session.add(self)
        self.save()

    def score(self):
        for player in self.players:
            player.score()

    def save(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Game %r>' % self.id
