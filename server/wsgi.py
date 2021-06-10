# -*- coding: utf-8 -*-
""" Web Server Gateway Interface  """

from os import getenv

from server.main.api import create_app_blueprint

# create and load `.env` file here from the respective environment to overwrite the env settings
# before app is created.

application = create_app_blueprint(getenv('FLASK_CONFIG') or 'default')
