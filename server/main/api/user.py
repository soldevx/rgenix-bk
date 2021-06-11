# -*- coding: utf-8 -*-
"""User Route for Demo application."""

from server.main.models.user import User
from flask import Blueprint

from server.main.services.user_service import UserService

route = Blueprint('user', __name__)

user_service = UserService()

@route.route("/api/users")
def test_db():
    user_service.save(User('George', 'george@gmail.com', 'password', True))
    return 'Success'