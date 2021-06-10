# -*- coding: utf-8 -*-
"""

UserService class - This class holds the method related to User manipulations.

"""

from server.main.models.jobdescs import Jobdesc
from server.main.models.cvs import CV
from server.main.services import SQLAlchemyService


class CVService(SQLAlchemyService):
    __model__ = CV

    def __init__(self):
        # Creating a parent class ref to access parent class methods.
        self.parentClassRef = super(CVService, self)

class JobdescService(SQLAlchemyService):
    __model__ = Jobdesc

    def __init__(self):
        # Creating a parent class ref to access parent class methods.
        self.parentClassRef = super(JobdescService, self)
