from app import db
from app.models.base import BaseMixin


class Roll(db.Model, BaseMixin):
    """
    The number of pins on a turn in bowling

    .. py:attribute:: pins

        The number of pins knocked down in a roll.

        :type: int

    """
    id = db.Column(db.Integer, primary_key=True)
    pins = db.Column(db.Integer)

    # for back ref
    frame_id = db.Column(db.Integer, db.ForeignKey('frame.id'))

    def __init__(self, frame, pins):
        self.pins = pins
        self.frame_id = frame.id
        db.session.add(self)


class Frame(db.Model, BaseMixin):
    """
    A frame in bowling.

    .. py:attribute:: number

        The fame number.

        :type: int

    .. py:attribute:: score

        The total score for the frame (this is a running total calculated from previous frames)

        :type: int

    .. py:attribute:: rolls

        A list of rolls in this frame.

        :type: A list of :py:class:`app.models.frame.Roll`

    """
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    score = db.Column(db.Integer)

    # for back ref
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

    rolls = db.relationship(
        'Roll', backref=db.backref('frame', lazy='joined'), lazy='dynamic')

    def __init__(self, player, number):
        self.number = number
        self.player_id = player.id
        db.session.add(self)

    def total_pins(self):
        """
        Helper method to get the total number of pins in this frame.

        :return: The total number of pins dropped in this frame.
        :rtype: int
        """
        return sum([roll.pins for roll in list(self.rolls.all())])

    def get_rolls(self):
        """
        Helper method to get the rolls in this frame.

        :return: The rolls for this frame.
        :rtype: A list of :py:class:`app.models.frame.Roll`
        """
        return list(self.rolls.all())

    def roll(self, pins):
        """
        Add a roll to this frame.

        :param int pins: The number of pins knocked over for this roll.
        :return: The roll that was added.
        :rtype: :py:class:`app.models.frame.Roll`
        :raises Exception: If the allowed number of rolls has been exceeded.
        """
        rolls = self.get_rolls()

        rolls_allowed = 2
        if self.number == 10 and len(rolls) and rolls[0].pins == 10:
            rolls_allowed = 3

        if len(rolls) >= rolls_allowed:
            raise Exception("Exceeded maximum rolls")

        roll = Roll(self, pins)
        roll.save()
        self.rolls.append(roll)
        return roll

    def is_strike(self):
        """
        Helper method to determine if this frame is a strike.

        :return: Truth
        :rtype: bool
        """
        if len(self.rolls.all()) == 1 and self.total_pins() == 10:
            return True
        return False

    def is_spare(self):
        """
        Helper method to determine if this frame is a spare.

        :return: Truth
        :rtype: bool
        """
        if len(self.rolls.all()) == 2 and self.total_pins() == 10:
            return True
        return False

    def is_complete(self):
        """
        Checks if this frame is complete.

        :return: Truth
        :rtype: bool
        """
        rolls = self.rolls.all()

        if self.number == 10:
            return self.is_complete10(rolls)
        return sum([roll.pins for roll in rolls]) == 10 or len(rolls) == 2

    def is_complete10(self, rolls):
        """
        Takes frame 10 into account when it checks if this frame is complete.

        :return: Truth
        :rtype: bool
        """
        n = len(rolls)

        if n < 3:
            return False

        # strike
        if n == 3 and rolls[0] == 10:
            return False
        return True

    def __repr__(self):
        return '<Frame %d %d>' % (self.id, self.score)
