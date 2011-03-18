#!/usr/bin/env python
# encoding: utf-8


import unittest
import Tree
import Datum
import Goal
import Actor
import Disclosure
import Mitigation
import Impact

class unittests(unittest.TestCase):
    def setUp(self):
        self.testTree1 = Tree()
        self.testTree2 = Tree()        
        self.testTree3 = Tree()

        self.testData1 = Datum('Test Data 1')
        self.testData2 = Datum('Test Data 2')
        self.testData3 = Datum('Test Data 3')
        self.testData4 = Datum('Test Data 4')
        self.testGoal1 = Goal('Test Goal 1')
        self.testGoal2 = Goal('Test Goal 2')
        self.testGoal3 = Goal('Test Goal 3')
        self.testGoal4 = Goal('Test Goal 4')
        self.testActor1 = Actor('Test Actor 1', [self.testGoal1, self.testGoal2], [self.testData1, self.testData2])
        self.testActor2 = Actor('Test Actor 2', [self.testGoal3, self.testGoal4], [self.testData3, self.testData4])
        self.testActors = {self.testActor1.name: self.testActor1, self.testActor2.name: self.testActor2}
        self.testDisclosure1 = Disclosure(self.testActor1, self.testData1, self.testActor2, 'Purpose 1')
        self.testDisclosure2 = Disclosure(self.testActor2, self.testData3, self.testActor1, 'Purpose 2')
        self.testDisclosures = [self.testDisclosure1, self.testDisclosure2]
        self.testMitigation1 = Mitigation(self.testDisclosure2, 'Anonymity', 'Test Mitigation Description 1')
        self.testMitigation2 = Mitigation(self.testDisclosure2, 'Limit Audience', 'Test Mitigation Desecription 2')
        self.testMitigation3 = Mitigation(self.testDisclosure1, 'Notice', 'Test Mitigation Desecription 3')
        self.testMitigations = [self.testMitigation1, self.testMitigation2, self.testMitigation3]
        self.testImpact1 = Impact(self.testMitigation2, 0)

        self.childData1 = Datum('Child Data 1')
        self.childData2 = Datum('Child Data 2')
        self.parentData = Datum('Parent Data 1')
        self.parentData.addChild(self.childData1)
        self.parentData.addChild(self.childData2)

        self.childGoal1 = Goal('Child Goal 1')
        self.childGoal2 = Goal('Child Goal 2')
        self.parentGoal = Goal('Parent Goal 1')
        self.parentGoal.addChild(self.childGoal1)
        self.parentGoal.addChild(self.childGoal2)

        self.childActor1 = Actor('Child Actor 1', [self.testGoal1], [self.testData1])
        self.childActor2 = Actor('Child Actor 2', [self.testGoal2], [self.testData2])
        self.parentActor = Actor('Parent Actor 1', [self.testGoal3], [self.testData3])
        self.parentActor.add(childActor1)
        self.parentActor.add(childActor2)

        self.testActor3 = Actor('Test Actor 3', [self.testGoal1], [self.parentData])
        self.testActor4 = Actor('Test Actor 4', [self.parentGoal], [self.testData1])
        self.nestedActors = {parentActor.name: parentActor, testActor3.name: testActor3, testActor4.name: testActor4}

    def test_tree(self):
        self.assertTrue(self.testTree1.parent == None)
        self.assertTrue(self.testTree1.children == [])
        self.testTree1.addChild(self.testTree2)
        self.assertTrue(self.testTree2 in self.testTree1.children)
        self.assertTrue(self.testTree2.parent == self.testTree1)
        self.testTree.removeChild(self.testTree2)
        self.assertTrue(self.testTree2.parent == None)
        self.assertTrue(self.testTree1.children == [])

    def test_data(self):
        self.assertEqual(self.testData1.name, 'Test Data 1')
        self.assertEqual(self.testData1.description, '')

    def test_nested_data(self):
        self.assertTrue(self.childData1 in self.parentData.children)
        self.assertTrue(self.childData2 in self.parentData.children)

    def test_goal(self):
        self.assertEqual(self.testGoal1.name, 'Test Goal 1')
        self.assertEqual(self.testGoal1.description, '')

    def test_nested_goals(self):
        self.assertTrue(self.childGoal1 in self.parentGoal.children)
        self.assertTrue(self.childGoal2 in self.parentGoal.children)

    def test_actor(self):
        self.assertEqual(self.testActor1.name, 'Test Actor 1')
        self.assertEqual(len(self.testActor1.goals), 2)
        self.assertEqual(self.testActor1.goals[0].name, 'Test Goal 1')
        self.assertEqual(len(self.testActor1.data), 2)
        self.assertEqual(self.testActor1.data[1].name, 'Test Data 2')
        self.assertEqual(self.testActors['Test Actor 1'].goals[0].name, 'Test Goal 1')

    def test_nested_actors(self):
        self.assertTrue(self.childActor1 in self.parentActor.children)
        self.assertTrue(self.childActor2 in self.parentActor.children)
        self.assertTrue(self.testGoal3 in self.childActor1.goals)
        self.assertTrue(self.testData3 in self.childActor2.data)
        self.assertFalse(self.testGoal2 in self.parentActor.goals)
        self.assertFalse(self.testdata2 in self.parentActor.data)

    def test_actors_with_nested_data(self):
        self.assertTrue(self.childData1 in self.testActor.data)
        self.assertTrue(self.childData2 in self.testActor.data)
        self.assertTrue(self.parentData in self.testActor.data)        

    def test_actors_with_nested_goals(self):
        self.assertTrue(self.childGoal1 in self.testActor.goal)
        self.assertTrue(self.childGoal2 in self.testActor.goal)
        self.assertTrue(self.parentGoal in self.testActor.goal)

    def test_disclosure(self):
        self.assertEqual(self.testDisclosure1.fromActor.name, 'Test Actor 1')
        self.assertEqual(self.testDisclosure2.purpose, 'Purpose 2')
        self.assertEqual(self.testDisclosures[1].toActor.name, 'Test Actor 1')

    def test_possible_disclosures(self):
        possibleDisclosures = getPossibleDisclosures(self.testActors)
        self.assertEqual(len(possibleDisclosures), 4)
        foundOne, foundTwo, foundThree, foundFour = False, False, False, False
        for d in possibleDisclosures:
            if d.fromActor.name == 'Test Actor 1' and d.toActor.name == 'Test Actor 2':
                if d.data.name == 'Test Data 1':
                    foundOne = True
                elif d.data.name == 'Test Data 2':
                    foundTwo = True
            elif d.fromActor.name == 'Test Actor 2' and d.toActor.name == 'Test Actor 1':
                if d.data.name == 'Test Data 3':
                    foundThree = True
                elif d.data.name == 'Test Data 4':
                    foundFour = True
        self.assertTrue(foundOne and foundTwo and foundThree and foundFour)
        self.testActors['Test Actor 3'] = Actor('Test Actor 3', [Goal('Test Goal 5')], [Datum('Test Data 6'), Datum('Test Data 7'), Datum('Test Data 8')])
        possibleDisclosures = getPossibleDisclosures(self.testActors)
        self.assertEqual(len(possibleDisclosures), 14)

    def test_nested_disclosures(self):
        possibleDisclsoures = getPossibleDisclosures(self.nestedActors)
        self.assertEqual(len(possibleDisclosures), 28)
        foundOne = False
        for d in possibleDisclsosures:
            if d.fromActor.name == 'Child Actor 1':
                if d.toActor.name == 'Test Actor 3':
                    if d.data.name == 'Test Data 3':
                        foundOne = True
        self.assertTrue(foundOne)

    def test_top_level_disclosures(self):
        topLevelDisclsoures = getTopLevelDisclosures(self.nestedActors)
        self.assertEqual(len(topLevelDisclosures), 6)
        foundOne = False
        for d in topLevelDisclsosures:
            if d.fromActor.name == 'Parent Actor':
                if d.toActor.name == 'Test Actor 3':
                    if d.data.name == 'Test Data 3':
                        foundOne = True
        self.assertTrue(foundOne)

    def test_mitigation(self):
        self.assertEqual(self.testMitigation1.disclosure.fromActor.name, 'Test Actor 2')
        self.assertEqual(self.testMitigation1.category, 'Anonymity')
        self.assertEqual(self.testMitigation1.description, 'Test Mitigation Description 1')
        self.assertEqual(self.testMitigations[2].category, 'Notice')

    def test_possible_mitigations(self):
        possibleMitigations = getPossibleMitigations(getPossibleDisclosures(self.testActors))
        self.assertEqual(len(possibleMitigations), 4 * len(mitigation_categories))

    def test_impact(self):
        self.assertEqual(self.testImpact1.mitigation.category, 'Limit Audience')
        self.assertEqual(self.testImpact1.actor.name, 'Test Actor 2')
        self.assertEqual(self.testImpact1.goal.name, 'Test Goal 3')

    def test_possible_goals(self):
        possibleImpacts = getPossibleImpacts(getPossibleMitigations(getPossibleDisclosures(self.testActors)))
        self.assertEqual(len(possibleImpacts), 4 * len(mitigation_categories) * 4)

    def p2pu(self):
        users = Actor('Learners', ['Learn about subjects using peer contributions', 'Contribute to others’ learning by asking helpful questions and providing feedback', 'Avoid revealing embarrassing or otherwise harmful information online'], ['Display Name', 'Username', 'First & last name', 'Email address', 'Password', 'Location', 'Bio', 'Profile image', 'Links', 'RSS feeds from links', 'Followers', 'Follower count', 'Following', 'Following count', 'Enrolled courses',  'Private messages', 'Clickstream/activity'])
        facilitators = Actor('Facilitators', ['Organize courses that are compelling and informative', 'Encourage feedback and student participation', 'Avoid revealing embarrassing or otherwise harmful information online'], [])
        organizers = Actor('Organizers', ['Create an open environment for learning', 'Bring high-quality learning material to as many people who want it as possible', 'Respect users by recognizing and appropriately treating sensitive information'], [])
        developers = Actor('Developers', ['Develop systems that are functional', 'Develop systems that are usable', 'Develop systems that are safe'], [])
        research = Actor('Research community', ['Conduct research and experiments that provide insight and guidance to academia and professional spheres', 'Follow ethical guidelines'], [])
        search = Actor('Search engines', ['Make all information on the web easily accessible to every web user', 'Follow sites directives with regards to spidering and storing information'], [])
        unregisteredUser = Actor('Unregistered users', ['Benefit from courses without directly participating'], [])
        isp = Actor('Internet service providers', ['Offer reliable, affordable service', 'Abide by local laws and regulations'], [])
        govt = Actor('Governments', ['Ensure safety and security'], [])
        actors = {users.name: users, developers.name: developers, isp.name: isp}
        for disclosure in getPossibleDisclosures(actors):
            print disclosure

if __name__ == '__main__':
    unittest.main()