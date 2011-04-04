#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy

uri = 'sqlite:///test.db'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    return app

db = SQLAlchemy(create_app())

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

class Datum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    
    def __init__(self, name, actor_id):
        self.name = name
        self.actor_id = actor_id

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    
    def __init__(self, name, actor_id):
        self.name = name
        self.actor_id = actor_id

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    app_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    data = db.relationship('Datum', backref=db.backref('actor'))
    goals = db.relationship('Goal', backref=db.backref('actor'))

    def __init__(self, name, app_id, data = [], goals = []):
        self.name = name
        self.app_id = app_id
        self.data = data
        self.goals = goals


class Disclosure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    
    from_actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    from_actor = db.relationship('Actor', primaryjoin=(from_actor_id==Actor.id), backref=db.backref('discloses'))
    
    to_actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    to_actor = db.relationship('Actor', primaryjoin=(to_actor_id==Actor.id), backref=db.backref('disclosed'))
    
    datum_id = db.Column(db.Integer, db.ForeignKey('datum.id'))
    datum = db.relationship('Datum', backref=db.backref('disclosure'))
    
    def __init__(self, app_id, from_actor_id, datum_id, to_actor_id, flagged = False):
        self.app_id = app_id
        self.from_actor_id = from_actor_id
        self.datum_id = datum_id
        self.to_actor_id = to_actor_id
        self.flagged = flagged

class Mitigation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    disclosure_id = db.Column(db.Integer, db.ForeignKey('disclosure.id'))
    disclosure = db.relationship('Disclosure', backref=db.backref('mitigation'))
    category = db.Column(db.String)
    def __init__(self, app_id, disclosure_id, category):
        self.app_id = app_id
        self.disclosure_id = disclosure_id
        self.category = category

class Impact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    mitigation_id = db.Column(db.Integer, db.ForeignKey('mitigation.id'))  
    mitigation = db.relationship('Mitigation', backref=db.backref('impact'))
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    goal = db.relationship('Goal', backref=db.backref('impact'))
    effect = db.Column(db.String)
    def __init__(self, app_id, mitigation_id, goal_id, effect):
        self.app_id = app_id
        self.mitigation_id = mitigation_id
        self.goal_id = goal_id
        self.effect = effect
        
def get_mitigations(effect, app_id):
    mitigations = []
    for m in Mitigation.query.all():
        support = Impact.query.filter('Impact.app_id == app_id').filter('Impact.mitigation_id == %d' % (m.id)).filter('effect == "support"').count()
        harm = Impact.query.filter('Impact.app_id == app_id').filter('Impact.mitigation_id == %d' % (m.id)).filter('effect == "harm"').count()
        if (support > harm and effect == 'support'):
            mitigations.append(m)
        elif (support < harm and effect == 'harm'):
            mitigations.append(m)
        elif (support == harm and effect == 'neutral'):
            mitigations.append(m)
    return mitigations
            
        
categories = ['Anonymity', 'Pseudonymity', 'Aggregation', 'Limited Audience', 'Notice', 'Choice']
effects = ['Support', 'Harm', 'No effect']