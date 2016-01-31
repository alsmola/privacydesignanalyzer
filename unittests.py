#!/usr/bin/env python
# encoding: utf-8

import unittest
from main import *
from flask.ext.testing import TestCase
from flask import Flask

class unittests(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        # pass in test configuration
        app = Flask(__name__)
        app.config['TESTING'] = True
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_datum(self):
        self.test_datum1 = Datum('Test Datum 1', 'actor_id')
        db.session.add(self.test_datum1)
        self.test_datum2 = Datum('Test Datum 2', 'actor_id')
        db.session.add(self.test_datum2)
        self.test_datum3 = Datum('Test Datum 3', 'actor_id')
        db.session.add(self.test_datum3)
        self.test_datum4 = Datum('Test Datum 4', 'actor_id')
        db.session.add(self.test_datum4)

        self.test_goal1 = Goal('Test Goal 1', 'actor_id')
        db.session.add(self.test_goal1)
        self.test_goal2 = Goal('Test Goal 2', 'actor_id')
        db.session.add(self.test_goal2)
        self.test_goal3 = Goal('Test Goal 3', 'actor_id')
        db.session.add(self.test_goal3)
        self.test_goal4 = Goal('Test Goal 4', 'actor_id')
        db.session.add(self.test_goal4)

        self.test_actor1 = Actor('Test Actor 1', 'app_id')
        db.session.add(self.test_actor1)
        self.test_actor2 = Actor('Test Actor 2', 'app_id')
        db.session.add(self.test_actor2)

        self.test_disclosure1 = Disclosure('app_id', self.test_actor1.id, self.test_datum1.id, self.test_actor2.id)
        db.session.add(self.test_disclosure1)
        self.test_disclosure2 = Disclosure('app_id', self.test_actor2.id, self.test_datum3.id, self.test_actor1.id)
        db.session.add(self.test_disclosure2)

        self.test_mitigation1 = Mitigation('app_id', self.test_disclosure2.id, 'Anonymity')
        db.session.add(self.test_mitigation1)
        self.test_mitigation2 = Mitigation('app_id', self.test_disclosure2.id, 'Limit Audience')
        db.session.add(self.test_mitigation2)
        self.test_mitigation3 = Mitigation('app_id', self.test_disclosure1.id, 'Notice')
        db.session.add(self.test_mitigation3)

        self.test_impact1 = Impact('app_id', self.test_mitigation2.id, self.test_actor1.id, self.test_goal2.id)
        db.session.add(self.test_impact1)
        self.test_impact2 = Impact('app_id', self.test_mitigation3.id, self.test_actor1.id, self.test_goal1.id)
        db.session.add(self.test_impact2)
        db.session.commit()
if __name__ == '__main__':
    unittest.main()
