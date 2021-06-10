# -*- coding: utf-8 -*-
'''Default api blueprints for connectivity testing.'''

from flask import Blueprint, jsonify

route = Blueprint('default', __name__)


@route.route('/api')
def hello():
    return 'Api is up and running.'

@route.route('/api/ping')
def ping():
    return jsonify({'status': 200, 'msg':'The ping was captured by the backend'})