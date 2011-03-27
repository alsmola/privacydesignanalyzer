#!/usr/bin/env python
# encoding: utf-8


import unittest
from main import *

class unittests(unittest.TestCase):
    def setUp(self):
        self.test_tree1 = Tree('Test Tree 1')
        self.test_tree2 = Tree('Test Tree 2')        
        self.test_tree3 = Tree('Test Tree 3')

        self.test_data1 = Datum('Test Data 1')
        self.test_data2 = Datum('Test Data 2')
        self.test_data3 = Datum('Test Data 3')
        self.test_data4 = Datum('Test Data 4')
        self.test_goal1 = Goal('Test Goal 1')
        self.test_goal2 = Goal('Test Goal 2')
        self.test_goal3 = Goal('Test Goal 3')
        self.test_goal4 = Goal('Test Goal 4')
        self.test_actor1 = Actor('Test Actor 1', Group([self.test_goal1, self.test_goal2]), Group([self.test_data1, self.test_data2]))
        self.test_actor2 = Actor('Test Actor 2', Group([self.test_goal3, self.test_goal4]), Group([self.test_data3, self.test_data4]))
        self.test_actors = Group([self.test_actor1, self.test_actor2])
        self.test_disclosure1 = Disclosure(self.test_actor1, self.test_data1, self.test_actor2, 'Purpose 1')
        self.test_disclosure2 = Disclosure(self.test_actor2, self.test_data3, self.test_actor1, 'Purpose 2')
        self.test_disclosures = [self.test_disclosure1, self.test_disclosure2]
        self.test_mitigation1 = Mitigation(self.test_disclosure2, 'Anonymity', 'Test Mitigation Description 1')
        self.test_mitigation2 = Mitigation(self.test_disclosure2, 'Limit Audience', 'Test Mitigation Desecription 2')
        self.test_mitigation3 = Mitigation(self.test_disclosure1, 'Notice', 'Test Mitigation Desecription 3')
        self.test_mitigations = [self.test_mitigation1, self.test_mitigation2, self.test_mitigation3]
        self.test_impact1 = Impact(self.test_mitigation2, self.test_actor1, self.test_goal2)
        self.test_impact2 = Impact(self.test_mitigation3, self.test_actor1, self.test_goal1)

        self.child_data1 = Datum('Child Data 1')
        self.child_data2 = Datum('Child Data 2')
        self.parent_data = Datum('Parent Data')
        self.parent_data.add_child(self.child_data1)
        self.parent_data.add_child(self.child_data2)

        self.child_goal1 = Goal('Child Goal 1')
        self.child_goal2 = Goal('Child Goal 2')
        self.parent_goal = Goal('Parent Goal')
        self.parent_goal.add_child(self.child_goal1)
        self.parent_goal.add_child(self.child_goal2)

        self.child_actor1 = Actor('Child Actor 1', Group([self.test_goal1]), Group([self.test_data1]))
        self.child_actor2 = Actor('Child Actor 2', Group([self.test_goal2]), Group([self.test_data2]))
        self.parent_actor = Actor('Parent Actor', Group([self.test_goal3]), Group([self.test_data3]))
        self.parent_actor.add_child(self.child_actor1)
        self.parent_actor.add_child(self.child_actor2)

        self.test_actor3 = Actor('Test Actor 3', Group([self.test_goal1]), Group([self.parent_data]))
        self.test_actor4 = Actor('Test Actor 4', Group([self.parent_goal]), Group([self.test_data1]))
        self.nested_actors = Group([self.parent_actor, self.test_actor3, self.test_actor4])

    def test_tree(self):
        self.assertTrue(self.test_tree1.parent == None)
        self.assertTrue(self.test_tree1.children == [])
        self.test_tree1.add_child(self.test_tree2)
        self.assertTrue(self.test_tree2 in self.test_tree1.children)
        self.assertTrue(self.test_tree2.parent == self.test_tree1)
        self.test_tree1.remove_child(self.test_tree2)
        self.assertTrue(self.test_tree2.parent == None)
        self.assertTrue(self.test_tree1.children == [])

    def test_group(self):
        self.assertEquals(self.test_actor1, self.test_actors.find('Test Actor 1'))
        self.assertTrue(self.test_actors.contains('Test Actor 2'))
        self.test_actors.remove('Test Actor 2')
        self.assertFalse(self.test_actors.contains('Test Actor 2'))
        self.assertEqual(len(self.test_actors.items), 1)
    
    def test_data(self):
        self.assertEqual(self.test_data1.name, 'Test Data 1')
        self.assertEqual(self.test_data1.description, '')

    def test_nested_data(self):
        self.assertTrue(self.child_data1 in self.parent_data.children)
        self.assertTrue(self.child_data2 in self.parent_data.children)

    def test_goal(self):
        self.assertEqual(self.test_goal1.name, 'Test Goal 1')
        self.assertEqual(self.test_goal1.description, '')

    def test_nested_goals(self):
        self.assertTrue(self.child_goal1 in self.parent_goal.children)
        self.assertTrue(self.child_goal2 in self.parent_goal.children)

    def test_actor(self):
        self.assertEqual(self.test_actor1.name, 'Test Actor 1')
        self.assertEqual(len(self.test_actor1.goals.items), 2)
        self.assertEqual(self.test_actor1.goals.items[0].name, 'Test Goal 1')
        self.assertEqual(len(self.test_actor1.data.items), 2)
        self.assertEqual(self.test_actor1.data.items[1].name, 'Test Data 2')
        self.assertEqual(self.test_actors.items[0].goals.items[0].name, 'Test Goal 1')

    def test_nested_actors(self):
        self.assertTrue(self.child_actor1 in self.parent_actor.children)
        self.assertTrue(self.child_actor2 in self.parent_actor.children)
        self.assertTrue(self.test_goal3 in self.child_actor1.goals.items)
        self.assertTrue(self.test_data3 in self.child_actor2.data.items)
        self.assertFalse(self.test_goal2 in self.parent_actor.goals.items)
        self.assertFalse(self.test_data2 in self.parent_actor.data.items)

    def test_actors_with_nested_data(self):
        self.assertTrue(self.child_data1 in self.test_actor3.data.items[0].children)
        self.assertTrue(self.child_data2 in self.test_actor3.data.items[0].children)
        self.assertTrue(self.parent_data in self.test_actor3.data.items)        

    def test_actors_with_nested_goals(self):
        self.assertTrue(self.child_goal1 in self.test_actor4.goals.items[0].children)
        self.assertTrue(self.child_goal2 in self.test_actor4.goals.items[0].children)
        self.assertTrue(self.parent_goal in self.test_actor4.goals.items)

    def test_get_all_actors(self):
        self.assertEqual(len(get_all_actors(self.test_actors).items), 2)
        self.assertEqual(len(get_all_actors(self.nested_actors).items), 5)

    def test_disclosure(self):
        self.assertEqual(self.test_disclosure1.from_actor.name, 'Test Actor 1')
        self.assertEqual(self.test_disclosure2.purpose, 'Purpose 2')
        self.assertEqual(self.test_disclosures[1].to_actor.name, 'Test Actor 1')

    def test_possible_disclosures(self):
        self.assertEqual(len(self.test_actors.items), 2)
        self.assertEqual(len(get_all_actors(self.test_actors).items), 2)
        possible_disclosures = get_possible_disclosures(self.test_actors)
        self.assertEqual(len(possible_disclosures), 4)
        found_one, found_two, found_three, found_four = False, False, False, False
        for d in possible_disclosures:
            if d.from_actor.name == 'Test Actor 1' and d.to_actor.name == 'Test Actor 2':
                if d.data.name == 'Test Data 1':
                    found_one = True
                elif d.data.name == 'Test Data 2':
                    found_two = True
            elif d.from_actor.name == 'Test Actor 2' and d.to_actor.name == 'Test Actor 1':
                if d.data.name == 'Test Data 3':
                    found_three = True
                elif d.data.name == 'Test Data 4':
                    found_four = True
        self.assertTrue(found_one and found_two and found_three and found_four)
        self.test_actors.add(Actor('Test Actor 3', Group([Goal('Test Goal 5')]), Group([Datum('Test Data 6'), Datum('Test Data 7'), Datum('Test Data 8')])))
        possible_disclosures = get_possible_disclosures(self.test_actors)
        self.assertEqual(len(possible_disclosures), 14)

    def test_nested_disclosures(self):
        possible_disclosures = get_possible_disclosures(self.nested_actors)
        self.assertEqual(len(possible_disclosures), 28)
        found_one = False
        for d in possible_disclosures:
            if d.from_actor.name == 'Child Actor 1':
                if d.to_actor.name == 'Test Actor 3':
                    if d.data.name == 'Test Data 3':
                        found_one = True
        self.assertTrue(found_one)

    def test_top_level_disclosures(self):
        top_level_disclosures = get_top_level_disclosures(self.nested_actors)
        self.assertEqual(len(top_level_disclosures), 6)
        found_one = False
        for d in top_level_disclosures:
            if d.from_actor.name == 'Parent Actor':
                if d.to_actor.name == 'Test Actor 3':
                    if d.data.name == 'Test Data 3':
                        found_one = True
        self.assertTrue(found_one)

    def test_trim_disclosures(self):
        self.test_data5 = Datum('Test Data 5')
        self.test_actor5 = Actor('Test Actor 5', Group([Goal('Test Goal 5')]), Group([self.test_data5]))
        self.test_actor6 = Actor('Test Actor 6', Group([Goal('Test Goal 6')]), Group([Datum('Test Data 6')]))
        self.test_actors.add(self.test_actor5)
        self.test_actors.add(self.test_actor6)
        disclosures = []
        disclosures.append(Disclosure(self.test_actor1, self.test_data1, self.test_actor2))
        disclosures.append(Disclosure(self.test_actor2, self.test_data3, self.test_actor5))
        disclosures.append(Disclosure(self.test_actor5, self.test_data5, self.test_actor6))
        self.test_actors.items.remove(self.test_actor2)
        possible_disclosures = get_possible_disclosures(self.test_actors)
        trimmed_disclosures = trim_disclosures(disclosures, possible_disclosures)
        self.assertEqual(len(trimmed_disclosures), 1)
        self.assertEqual(trimmed_disclosures[0].from_actor, self.test_actor5)
        self.assertEqual(trimmed_disclosures[0].to_actor, self.test_actor6)

    def test_find_disclosure(self):
        disclosure = find_disclosure('Test Actor 1', 'Test Data 1', 'Test Actor 2', self.test_actors, self.test_disclosures)
        self.assertEqual(disclosure, self.test_disclosure1)
    
    def test_create_disclosure(self):
        disclosure = create_disclosure('Test Actor 2', 'Test Data 3', 'Test Actor 1', self.test_actors)
        self.assertEqual(disclosure, self.test_disclosure2)
    
    def test_mitigation(self):
        self.assertEqual(self.test_mitigation1.disclosure.from_actor.name, 'Test Actor 2')
        self.assertEqual(self.test_mitigation1.category, 'Anonymity')
        self.assertEqual(self.test_mitigation1.description, 'Test Mitigation Description 1')
        self.assertEqual(self.test_mitigations[2].category, 'Notice')

    def test_possible_mitigations(self):
        possible_mitigations = get_possible_mitigations(get_possible_disclosures(self.test_actors))
        self.assertEqual(len(possible_mitigations), 4 * len(mitigation_categories))

    def test_trim_mitigations(self):
        self.test_data5 = Datum('Test Data 5')
        self.test_actor5 = Actor('Test Actor 5', Group([Goal('Test Goal 5')]), Group([self.test_data5]))
        self.test_actor6 = Actor('Test Actor 6', Group([Goal('Test Goal 6')]), Group([Datum('Test Data 6')]))
        self.test_actors.add(self.test_actor5)
        self.test_actors.add(self.test_actor6)
        self.test_disclosure1 = Disclosure(self.test_actor1, self.test_data1, self.test_actor2)
        self.test_disclosure2 = Disclosure(self.test_actor2, self.test_data3, self.test_actor5)
        self.test_disclosure3 = Disclosure(self.test_actor5, self.test_data5, self.test_actor6)
        disclosures = [self.test_disclosure1, self.test_disclosure2, self.test_disclosure3]
        self.test_mitigation1 = Mitigation(self.test_disclosure1, 'Limitation of Audience')
        self.test_mitigation2 = Mitigation(self.test_disclosure3, 'Anonymity')
        mitigations = [self.test_mitigation1, self.test_mitigation2]    
        self.test_actors.items.remove(self.test_actor2)
        possible_disclosures = get_possible_disclosures(self.test_actors)
        trimmed_disclosures = trim_disclosures(disclosures, possible_disclosures)
        trimmed_mitigations = trim_mitigations(mitigations, trimmed_disclosures)
        self.assertEqual(len(trimmed_mitigations), 1)
        self.assertEqual(trimmed_mitigations[0].disclosure, self.test_disclosure3)
        self.assertEqual(trimmed_mitigations[0].category, 'Anonymity')
        
    def test_impact(self):
        self.assertEqual(self.test_impact1.mitigation.category, 'Limit Audience')
        self.assertEqual(self.test_impact1.actor.name, 'Test Actor 1')
        self.assertEqual(self.test_impact1.goal.name, 'Test Goal 2')

    def test_trim_impacts(self):
        self.test_data5 = Datum('Test Data 5')
        self.test_actor5 = Actor('Test Actor 5', Group([Goal('Test Goal 5')]), Group([self.test_data5]))
        self.test_actor6 = Actor('Test Actor 6', Group([Goal('Test Goal 6')]), Group([Datum('Test Data 6')]))
        self.test_actors.add(self.test_actor5)
        self.test_actors.add(self.test_actor6)
        self.test_disclosure1 = Disclosure(self.test_actor1, self.test_data1, self.test_actor2)
        self.test_disclosure2 = Disclosure(self.test_actor2, self.test_data3, self.test_actor5)
        self.test_disclosure3 = Disclosure(self.test_actor5, self.test_data5, self.test_actor6)
        disclosures = [self.test_disclosure1, self.test_disclosure2, self.test_disclosure3]
        self.test_mitigation1 = Mitigation(self.test_disclosure1, 'Limitation of Audience')
        self.test_mitigation2 = Mitigation(self.test_disclosure3, 'Anonymity')
        mitigations = [self.test_mitigation1, self.test_mitigation2]    
        self.test_impact1 = Impact(self.test_mitigation1, self.test_actor1, self.test_goal1, 'Support')
        self.test_impact2 = Impact(self.test_mitigation2, self.test_actor2, self.test_goal3, 'Harm')
        impacts = [self.test_impact1, self.test_impact2]
        self.test_actors.items.remove(self.test_actor5)
        possible_disclosures = get_possible_disclosures(self.test_actors)
        trimmed_disclosures = trim_disclosures(disclosures, possible_disclosures)
        trimmed_mitigations = trim_mitigations(mitigations, trimmed_disclosures)
        trimmed_impacts = trim_impacts(impacts, trimmed_mitigations, self.test_actors)
        self.assertEqual(len(trimmed_impacts), 1)
        self.assertEqual(trimmed_impacts[0].effect, 'Support')
        self.test_actor1.goals.items.remove(self.test_goal1)
        possible_disclosures = get_possible_disclosures(self.test_actors)
        trimmed_disclosures = trim_disclosures(disclosures, possible_disclosures)
        trimmed_mitigations = trim_mitigations(mitigations, trimmed_disclosures)
        trimmed_impacts = trim_impacts(impacts, trimmed_mitigations, self.test_actors)
        self.assertEqual(len(trimmed_impacts), 0)


if __name__ == '__main__':
    unittest.main()