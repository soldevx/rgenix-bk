# -*- coding: utf-8 -*-
from server.main.models.user import *
from sqlalchemy import ForeignKey


class Jobdesc(BaseModel, db.Model):
    '''Model for Job descriptions table'''
    __tablename__ = 'jobdescs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pdf_binary = db.Column(db.LargeBinary, nullable=False)
    preproc1 = db.Column(db.UnicodeText, nullable=False)
    preproc2 = db.Column(db.UnicodeText, nullable = False)
    uid = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, pdf_binary, preproc1, preproc2, uid):
        super().__init__()
        self.pdf_binary = pdf_binary
        self.preproc1 = preproc1
        self.preproc2 = preproc2
        self.uid = uid