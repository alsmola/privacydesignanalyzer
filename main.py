#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

class Datum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    
    def __init__(self, name):
        self.name = name

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    
    def __init__(self, name):
        self.name = name

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    app_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    data = db.relationship('Datum', backref=db.backref('actor', lazy='dynamic'))
    goals = db.relationship('Goal', backref=db.backref('actor', lazy='dynamic'))

    def __init__(self, name, datum, goals):
        self.name = name
        self.data = data
        self.goals = goals

class Disclosure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    to_actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    datum_id = db.Column(db.Integer, db.ForeignKey('datum.id'))
    flagged = db.Column(db.Boolean)
    def __init__(self, from_actor_id, data_id, to_actor_id, flagged = False):
        self.from_actor_id = from_actor_id
        self.data_id = data_id
        self.to_actor_id = to_actor_id
        self.flagged = flagged

class Mitigation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disclosure_id = db.Column(db.Integer, db.ForeignKey('disclosure.id'))
    category = db.Column(db.String)
    def __init__(self, disclosure_id, category, flagged = False):
        self.disclosure_id = disclosure_id
        self.category = category
        self.description = description
        self.flagged = flagged

class Impact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mitigation_id = db.Column(db.Integer, db.ForeignKey('disclosure.id'))
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    effect = db.Column(db.String)
    def __init__(self, mitigation_id, goal_id, effect):
        self.mitigation_id = mitigation_id
        self.goal_id = goal_id
        self.effect = effect
        
categories = ['Anonymity', 'Pseudonymity', 'Aggregation', 'Limited Audience', 'Notice', 'Choice']
effects = ['Support', 'Harm', 'No effect']