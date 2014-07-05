from app import db


class BaseMixin(object):
    """
    Base class for all model classes written as a mix in, because deriving db.Model
    doesn't work (probably do to introspecting the database tables).
    """

    def save(self):
        """
        Commit the model to the database
        """
        db.session.commit()

    def __repr__(self):
        return '<{} {}>' % (self.__class__.__name__, self.id)
