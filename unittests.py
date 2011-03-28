#!/usr/bin/env python
# encoding: utf-8


import unittest
from main import *
from db import session # probably a contextbound sessionmaker
from db import model

from sqlalchemy import create_engine

class unittests(unittest.TestCase):
    
    def setup():
        db = create_engine('sqlite:///:memory:')
        session.configure(bind=engine)
        main.create_all(db)
        
        self.test_datum1 = Datum('Test Datum 1')
        session.add(self.test_datum1)
        self.test_datum2 = Datum('Test Datum 2')
        session.add(self.test_datum2)
        self.test_datum3 = Datum('Test Datum 3')
        session.add(self.test_datum3)
        self.test_datum4 = Datum('Test Datum 4')
       session.add(self.test_datum4)
        
        self.test_goal1 = Goal('Test Goal 1')
        session.add(self.test_goal1)        
        self.test_goal2 = Goal('Test Goal 2')
        session.add(self.test_goal2)
        self.test_goal3 = Goal('Test Goal 3')
        session.add(self.test_goal3)
        self.test_goal4 = Goal('Test Goal 4')
        session.add(self.test_goal4)
       
        self.test_actor1 = Actor('Test Actor 1', [self.test_goal1, self.test_goal2]), [self.test_datum1, self.test_datum2])
        session.add(self.test_actor1)
        self.test_actor2 = Actor('Test Actor 2', [self.test_goal3, self.test_goal4]), [self.test_datum3, self.test_datum4])
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
              

    def teardown():
        session.remove()

    def test_datum(self):
        instances = session.query(Datum).all()
        eq_(0, len(instances))
        self.assertEqual(self.test_datum1.name, 'Test Datum 1')
        self.assertEqual(self.test_datum1.description, '')

    def test_goal(self):
        self.assertEqual(self.test_goal1.name, 'Test Goal 1')
        self.assertEqual(self.test_goal1.description, '')

    def test_actor(self):
        self.assertEqual(self.test_actor1.name, 'Test Actor 1')
        self.assertEqual(len(self.test_actor1.goals.items), 2)
        self.assertEqual(self.test_actor1.goals.items[0].name, 'Test Goal 1')
        self.assertEqual(len(self.test_actor1.data.items), 2)
        self.assertEqual(self.test_actor1.data.items[1].name, 'Test Datum 2')
        self.assertEqual(self.test_actors.items[0].goals.items[0].name, 'Test Goal 1')

    def test_disclosure(self):
        self.assertEqual(self.test_disclosure1.from_actor.name, 'Test Actor 1')
        self.assertEqual(self.test_disclosure2.purpose, 'Purpose 2')
        self.assertEqual(self.test_disclosures[1].to_actor.name, 'Test Actor 1')

    def test_mitigation(self):
        self.assertEqual(self.test_mitigation1.disclosure.from_actor.name, 'Test Actor 2')
        self.assertEqual(self.test_mitigation1.category, 'Anonymity')
        self.assertEqual(self.test_mitigation1.description, 'Test Mitigation Description 1')
        self.assertEqual(self.test_mitigations[2].category, 'Notice')

    def test_impact(self):
        self.assertEqual(self.test_impact1.mitigation.category, 'Limit Audience')
        self.assertEqual(self.test_impact1.actor.name, 'Test Actor 1')
        self.assertEqual(self.test_impact1.goal.name, 'Test Goal 2')

if __name__ == '__main__':
    unittest.main()