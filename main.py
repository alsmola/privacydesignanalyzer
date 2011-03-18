#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest

class Tree:
    def __init__(self):
        self.children = []
        self.parent = None
        
    def addChild(child):        
        if child in self.children:
            raise Exception('Value alredy in tree.')
        if child.parent != None:
            raise Exception('Child already has a parent.')
        self.children.append(child)
        child.parent = self
    
    def removeChild(child):
        if not child in self.children:
            raise Exception('Child not in tree.')
        if child.parent == None:
            raise Exception('Child does not have parent.')
        self.children.remove(child)
        child.parent = None

class Datum(Tree):
    def __init__(self, name, description = ''):
        self.name = name
        self.description = description
    def __str__(self):
        return self.name

class Goal(Tree):
    def __init__(self, name, description = ''):
        self.name = name
        self.description = description
    def __str__(self):
        return self.name

class Actor(Tree):
    def __init__(self, name, goals, data):
        self.name = name
        self.goals = goals
        self.data = data   
    def __str__(self):
        return self.name

class Disclosure:
    def __init__(self, fromActor, data, toActor, purpose = '', flagged = False):
        self.fromActor = fromActor
        self.data = data
        self.toActor = toActor
        self.purpose = purpose
        self.flagged = flagged
    def __str__(self):
        return "disclosure of %s from %s to %s for %s" % (self.data, self.fromActor, self.toActor, self.purpose)
    
class Mitigation:
    def __init__(self, disclosure, category, description = '', flagged = False):
        self.disclosure = disclosure
        self.category = category
        self.description = description
        self.flagged = flagged
    def __str__(self):
        return "mitigation of %s by %s, where %s" % (self.disclosure, self.category, self.description)

class Impact:
    def __init__(self, mitigation, goalIndex, effect = 'None'):
        self.mitigation = mitigation
        if goalIndex < len(mitigation.disclosure.fromActor.goals):
            actor = mitigation.disclosure.fromActor
            goalIndex = goalIndex
        else:
            actor = mitigation.disclosure.toActor
            goalIndex = goalIndex - len(mitigation.disclosure.fromActor.goals)
        self.actor = actor
        self.goal = actor.goals[goalIndex]
        self.effect = effect
        
    def __str__(self):
        return 'for mitigation: %s, the goal: %s for actor: %s is affected: %s' % (self.mitigation, self.goal, self.actor, self.effect)
        

mitigation_categories = ['Anonymity', 'Pseudonymity', 'Aggregation', 'Limited Audience', 'Notice', 'Choice']

def getPossibleDisclosures(actors):
    disclosures = []
    for toActorName, toActor in actors.iteritems():
        for data in toActor.data:
            for fromActorName, fromActor in actors.iteritems():
                if fromActor.name != toActor.name:
                    disclosures.append(Disclosure(toActor, data, fromActor))
    return disclosures

def getTopLevelDisclosures(actors):
    disclosures = []
    for toActorName, toActor in actors.iteritems():
        if toActor.chidren != []:
            for data in toActor.data:
                if data.children != []:
                    for fromActorName, fromActor in actors.iteritems():
                        if fromActor.children != []:
                            if fromActor.name != toActor.name:
                                disclosures.append(Disclosure(toActor, data, fromActor))
    return disclosures

def getPossibleMitigations(disclosures):
    mitigations = []
    for disclosure in disclosures:
        for category in mitigation_categories:
            mitigations.append(Mitigation(disclosure, category))
    return mitigations

def getPossibleImpacts(mitigations):
    impacts = []
    for mitigation in mitigations:
        goalIndex = 0
        for goal in mitigation.disclosure.fromActor.goals:
            impacts.append(Impact(mitigation, goalIndex))
            goalIndex = goalIndex + 1            
        for goal in mitigation.disclosure.toActor.goals:
            impacts.append(Impact(mitigation, goalIndex))
            goalIndex = goalIndex + 1
    return impacts

