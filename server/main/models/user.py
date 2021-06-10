# -*- coding: utf-8 -*-
from server.main.models.base import *


class User(BaseModel, db.Model):
    '''Model for users table'''
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=func.now())
    company = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, email, password, company):
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
        self.company = company
