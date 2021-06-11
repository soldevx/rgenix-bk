# -*- coding: utf-8 -*-
from flask_script import Manager

from server.main import db
from server.main.api import create_app_blueprint

# create flask application instance
app = create_app_blueprint('development')
manager = Manager(app)

@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    manager.run()
