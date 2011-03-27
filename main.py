#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest

class Group:
    def __init__(self, items = []):
        self.items = items
    
    def add(self, item):
        result = self.find(item.name)
        if result != None:
            return 'Error: %s with name "%s" already exists.' % (type(item), item.name)
        self.items.append(item)

    def remove(self, name):
        result = self.find(name)
        if result == None:
            return 'Error: %s with name "%s" does not exist.' % (type(item), name)
        self.items.remove(result)
    
    def update(self, name, new_name):
        if (self.contains(new_name)):
            return 'Error: %s with name "%s" already exists.' % (type(item), name)
        result = find(name)
        if (result == None):
            return 'Error: %s with name "%s" does not exist.' % (type(item), name)
        result.name = new_name 
    
    def find(self, name):
        for i in self.items:
            if (i.name == name):
                return i
        return None

    def contains(self, name):
        return (self.find(name) != None)

class Tree:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None
     
    def __eq__(self, other):
        if (other is None or self is None):
            return (other is None and self is None)
        return self.name == other.name and type(self) == type(other)
    
    def __str__(self):
        return self.name
                
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
        Tree.__init__(self, name)
        self.description = description

class Goal(Tree):
    def __init__(self, name, description = ''):
        Tree.__init__(self, name)
        self.description = description

class Actor(Tree):
    def __init__(self, name, goals = Group([]), data = Group([])):
        Tree.__init__(self, name)
        self._goals = goals
        self._data = data   

    def get_data(self):
        all_data = self._data
        if (self.parent != None):
            for d in self.parent.data.items:
                all_data.add(d)
        return all_data
    
    def set_data(self, value):
        self._data = value

    def get_goals(self):
        all_goals = self._goals
        if (self.parent != None):
            for g in self.parent.goals.items:
                all_goals.add(g)
        return all_goals
     
    def set_goals(self, value):
        self._goals = value
     
    data = property(get_data, set_data)
    goals = property(get_goals, set_goals)


class Disclosure:
    def __init__(self, from_actor, data, to_actor, purpose = '', flagged = False):
        self.from_actor = from_actor
        self.data = data
        self.to_actor = to_actor
        self.purpose = purpose
        self.flagged = flagged
    
    def __eq__ (self, other):
        if (other is None or self is None):
            return (other is None and self is None)
        return self.from_actor == other.from_actor and self.data == other.data and self.to_actor == other.to_actor
    
    def __str__(self):
        if (self.purpose == ''):
            return "disclosure of %s from %s to %s" % (self.data, self.from_actor, self.to_actor)            
        else:
            return "disclosure of %s from %s to %s for %s" % (self.data, self.from_actor, self.to_actor, self.purpose)
class Mitigation:
    def __init__(self, disclosure, category, description = '', flagged = False):
        self.disclosure = disclosure
        self.category = category
        self.description = description
        self.flagged = flagged

    def __eq__ (self, other):
        if (other is None or self is None):
            return (other is None and self is None)
        return self.disclosure == other.disclosure and self.category == other.category
        
    def __str__(self):
        return "mitigation of %s by %s, where %s" % (self.disclosure, self.category, self.description)

class Impact:
    def __init__(self, mitigation, actor, goal, effect = 'None'):
        self.mitigation = mitigation
        self.actor = actor
        self.goal = goal
        self.effect = effect
    
    def __eq__ (self, other):
        if (other is None or self is None):
            return (other is None and self is None)
        return self.mitigation == other.mitigation and self.actor == other.actor and self.goal == other.goal
    def __str__(self):
        return 'for mitigation: %s, the goal: %s for actor: %s is affected: %s' % (self.mitigation, self.goal, self.actor, self.effect)
        

mitigation_categories = ['Anonymity', 'Pseudonymity', 'Aggregation', 'Limited Audience', 'Notice', 'Choice']

def get_all_actors(actors):
    items = []
    all_actors = Group([])
    for actor in actors.items:
        all_actors.add(actor)
        if actor.children != []:
            for child in actor.children:
                all_actors.add(child)
    return all_actors

def get_possible_disclosures(actors):
    disclosures = []
    for to_actor in get_all_actors(actors).items:
        for data in to_actor.data.items:
            for from_actor in get_all_actors(actors).items:
                if from_actor != to_actor:
                    disclosures.append(Disclosure(to_actor, data, from_actor))
    return disclosures

def get_top_level_disclosures(actors):
    disclosures = []
    for to_actor in actors.items:
        for data in to_actor.data.items:
            if data.parent == None:
                for from_actor in actors.items:
                    if from_actor.name != to_actor.name:
                        disclosures.append(Disclosure(to_actor, data, from_actor))
    return disclosures

def trim_disclosures(disclosures, possible_disclosures):
    new_disclosures = []
    for disclosure in disclosures:
        for possible_disclosure in possible_disclosures:
            if possible_disclosure == disclosure:
                    new_disclosures.append(disclosure)
    return new_disclosures

def find_disclosure(from_actor_name, data_name, to_actor_name, actors, disclosures):
    check = create_disclosure(from_actor_name, data_name, to_actor_name, actors)
    for d in disclosures:
        if d == check:
            return d
    return None
    
def create_disclosure(from_actor_name, data_name, to_actor_name, actors):
    from_actor = actors.find(from_actor_name)
    data = from_actor.data.find(data_name)
    to_actor = actors.find(to_actor_name)
    if (from_actor == None or data == None or to_actor == None):
        return 'Error: disclosure relies on missing actors or data.'
    return Disclosure(from_actor, data, to_actor)   
    
def get_possible_mitigations(disclosures):
    mitigations = []
    for disclosure in disclosures:
        for category in mitigation_categories:
            mitigations.append(Mitigation(disclosure, category))
    return mitigations

def trim_mitigations(mitigations, trimmed_disclosures):
    new_mitigations = []
    for mitigation in mitigations:
        for disclosure in trimmed_disclosures:
            if disclosure ==  mitigation.disclosure:
                new_mitigations.append(mitigation)
    return new_mitigations
    
def trim_impacts(impacts, trimmed_mitigations, actors):
    new_impacts = []
    for impact in impacts:
        for mitigation in trimmed_mitigations:
            if mitigation == impact.mitigation:
                for actor in actors.items:
                    for goal in actor.goals.items:
                        if goal == impact.goal:
                            new_impacts.append(impact)
    return new_impacts