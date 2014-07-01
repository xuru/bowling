from flask.ext.testing import TestCase
from app import app, db


class BaseTest(TestCase):

    def create_app(self):
        print "Create app..."
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/apply_test.db'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        print "setUp"
        db.create_all()

    def tearDown(self):
        print "tearDown"
        db.session.remove()
        db.drop_all()
