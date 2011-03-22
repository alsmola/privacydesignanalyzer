#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest

class Tree:
    def __init__(self):
        self.children = []
        self.parent = None
        
    def add_child(self, child):        
        if child in self.children:
            raise Exception('Value alredy in tree.')
        if child.parent != None:
            raise Exception('Child already has a parent.')
        self.children.append(child)
        child.parent = self
    
    def remove_child(self, child):
        if not child in self.children:
            raise Exception('Child not in tree.')
        if child.parent == None:
            raise Exception('Child does not have parent.')
        self.children.remove(child)
        child.parent = None

class Datum(Tree):
    def __init__(self, name, description = ''):
        Tree.__init__(self)
        self.name = name
        self.description = description
    def __str__(self):
        return self.name

class Goal(Tree):
    def __init__(self, name, description = ''):
        Tree.__init__(self)
        self.name = name
        self.description = description
    def __str__(self):
        return self.name

class Actor(Tree):
    def __init__(self, name, goals = [], data = []):
        Tree.__init__(self)
        self.name = name
        self._goals = goals
        self._data = data   

    def get_data(self):
        all_data = self._data
        if (self.parent != None):
            for d in self.parent.data:
                all_data.append(d)
        return all_data
    
    def set_data(self, value):
        self._data = value

    def get_goals(self):
        all_goals = self._goals
        if (self.parent != None):
            for g in self.parent.goals:
                all_goals.append(g)
        return all_goals
     
    def set_goals(self, value):
        self._goals = value
     
    data = property(get_data, set_data)
    goals = property(get_goals, set_goals)
        
    def __str__(self):
        return self.name

class Disclosure:
    def __init__(self, from_actor, data, to_actor, purpose = '', flagged = False):
        self.from_actor = from_actor
        self.data = data
        self.to_actor = to_actor
        self.purpose = purpose
        self.flagged = flagged
    def __str__(self):
        return "disclosure of %s from %s to %s for %s" % (self.data, self.from_actor, self.to_actor, self.purpose)
    
class Mitigation:
    def __init__(self, disclosure, category, description = '', flagged = False):
        self.disclosure = disclosure
        self.category = category
        self.description = description
        self.flagged = flagged
    def __str__(self):
        return "mitigation of %s by %s, where %s" % (self.disclosure, self.category, self.description)

class Impact:
    def __init__(self, mitigation, goal_index, effect = 'None'):
        self.mitigation = mitigation
        if goal_index < len(mitigation.disclosure.from_actor.goals):
            actor = mitigation.disclosure.from_actor
            goal_index = goal_index
        else:
            actor = mitigation.disclosure.to_actor
            goal_index = goal_index - len(mitigation.disclosure.from_actor.goals)
        self.actor = actor
        self.goal = actor.goals[goal_index]
        self.effect = effect
        
    def __str__(self):
        return 'for mitigation: %s, the goal: %s for actor: %s is affected: %s' % (self.mitigation, self.goal, self.actor, self.effect)
        

mitigation_categories = ['Anonymity', 'Pseudonymity', 'Aggregation', 'Limited Audience', 'Notice', 'Choice']

def get_all_actors(actors):
    all_actors = []
    for actor in actors:
        all_actors.append(actor)
        if actor.children != []:
            for child in actor.children:
                all_actors.append(child)
    return all_actors

def get_possible_disclosures(actors):
    disclosures = []
    for to_actor in get_all_actors(actors):
        for data in to_actor.data:
            for from_actor in get_all_actors(actors):
                if from_actor.name != to_actor.name:
                    disclosures.append(Disclosure(to_actor, data, from_actor))
    return disclosures

def get_top_level_disclosures(actors):
    disclosures = []
    for to_actor in actors:
        for data in to_actor.data:
            if data.parent == None:
                for from_actor in actors:
                    if from_actor.name != to_actor.name:
                        disclosures.append(Disclosure(to_actor, data, from_actor))
    return disclosures

def get_possible_mitigations(disclosures):
    mitigations = []
    for disclosure in disclosures:
        for category in mitigation_categories:
            mitigations.append(Mitigation(disclosure, category))
    return mitigations

def get_possible_impacts(mitigations):
    impacts = []
    for mitigation in mitigations:
        goalIndex = 0
        for goal in mitigation.disclosure.from_actor.goals:
            impacts.append(Impact(mitigation, goalIndex))
            goalIndex = goalIndex + 1            
        for goal in mitigation.disclosure.to_actor.goals:
            impacts.append(Impact(mitigation, goalIndex))
            goalIndex = goalIndex + 1
    return impacts