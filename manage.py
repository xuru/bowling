import os.path
import subprocess
from flask.ext.script import Manager
from app import app, db

HERE = os.path.abspath(os.path.dirname(__file__))
manager = Manager(app)


@manager.command
def serve():
    db.create_all()
    app.run(debug=True)


@manager.command
def docs():
    subprocess.call('cd docs && make html && /usr/bin/open build/html/index.html', shell=True)


if __name__ == "__main__":
    manager.run()
