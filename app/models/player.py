from app import db
from app.models import Frame


class Player(db.Model):
    """
    The player in a game of bowling.
    name: The players name
    frames: The bowling frames that may or may not be scored yet.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

    frames = db.relationship(
        'Frame', backref=db.backref('player', lazy='joined'), lazy='dynamic')

    def __init__(self, game, name):
        self.name = name
        self.game_id = game.id
        db.session.add(self)

        index = 0
        while len(list(self.frames.all())) != 10:
            Frame(self, index).save()
            index += 1

    def save(self):
        db.session.commit()

    def score(self):
        """
        Score all the frames, and save them to the db.
        """
        result = []
        frames = list(self.frames.all())

        # create a flat array of rolls
        rolls = []
        for frame in frames:
            rolls.extend([roll.pins for roll in frame.get_rolls()])

        pos = -1
        for i, frame in enumerate(frames):
            bonus = 0
            if frame.is_strike():
                pos += 1
                if pos+3 > len(rolls):
                    bonus = sum(rolls[pos+1:])
                else:
                    bonus = sum(rolls[pos+1:pos+3])
            elif frame.is_spare():
                pos += 2
                bonus = sum(rolls[pos+1:pos+2])
            else:
                pos += len(frame.get_rolls())

            prev = result[i - 1] if result else 0

            frame.score = prev + frame.total_pins() + bonus
            frame.save()

            result.append(frame.score)
        return result

    def roll(self, pins):
        """
        Does some initial validation before calling the current frames roll() method.
        """
        if pins > 10 or pins < 0:
            raise Exception("Wrong number of pins")

        found = False
        frames = list(self.frames.all())
        for frame in frames:
            if not frame.is_complete():
                found = True
                break

        if found:
            return frame.roll(pins)

    def __repr__(self):
        return '<Player %d %s>' % (self.id, self.name)
