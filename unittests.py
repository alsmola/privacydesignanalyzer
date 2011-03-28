#!/usr/bin/env python
# encoding: utf-8

from main import *
from flaskext.testing import TestCase

class unittests(TestCase):
    
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        # pass in test configuration
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_datum(self):  
        self.test_datum1 = Datum('Test Datum 1')
        session.add(self.test_datum1)
        self.test_datum2 = Datum('Test Datum 2')
        session.add(self.test_datum2)
        self.test_datum3 = Datum('Test Datum 3')
        session.add(self.test_datum3)
        self.test_datum4 = Datum('Test Datum 4')
        session.add(self.test_datum4)
        
        self.test_goal1 = Goal('Test Goal 1')
        session.add(self.test_goal1)        
        self.test_goal2 = Goal('Test Goal 2')
        session.add(self.test_goal2)
        self.test_goal3 = Goal('Test Goal 3')
        session.add(self.test_goal3)
        self.test_goal4 = Goal('Test Goal 4')
        session.add(self.test_goal4)
       
        self.test_actor1 = Actor('Test Actor 1', [self.test_goal1, self.test_goal2], [self.test_datum1, self.test_datum2])
        session.add(self.test_actor1)
        self.test_actor2 = Actor('Test Actor 2', [self.test_goal3, self.test_goal4], [self.test_datum3, self.test_datum4])
        session.add(self.test_actor2)

        self.test_disclosure1 = Disclosure(self.test_actor1.id, self.test_datum1.id, self.test_actor2.id)
        session.add(self.test_disclosure1)
        self.test_disclosure2 = Disclosure(self.test_actor2.id, self.test_datum3.id, self.test_actor1.id)
        session.add(self.test_disclosure2)

        self.test_mitigation1 = Mitigation(self.test_disclosure2.id, 'Anonymity')
        session.add(self.test_mitigation1)
        self.test_mitigation2 = Mitigation(self.test_disclosure2.id, 'Limit Audience')
        session.add(self.test_mitigation2)
        self.test_mitigation3 = Mitigation(self.test_disclosure1.id, 'Notice')
        session.add(self.test_mitigation3)

        self.test_impact1 = Impact(self.test_mitigation2.id, self.test_actor1.id, self.test_goal2.id)
        session.add(self.test_impact1)
        self.test_impact2 = Impact(self.test_mitigation3.id, self.test_actor1.id, self.test_goal1.id)
        session.add(self.test_impact2)
        
        session.commit()
     
if __name__ == '__main__':
    unittest.main()