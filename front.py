from flask import Flask, render_template, request, session
import main
from main import Actor, Goal, Datum, Disclosure, Mitigation, Impact
app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/actors", methods=['GET',])
def actors():
    return render_template('actors.html', actors = session['actors'])

@app.route('/actor', methods=['POST',])
def actor():
    name = request.form['name']
    verb = request.form['verb']
    if verb == 'create':
        for actor in session['actors']:
            if (actor.name == name):
                return 'Error: actor with name "%s" already exists.' % (name)
        session['actors'].append(Actor(name))
    elif verb == 'edit' or verb == 'delete':
        a = None
        for actor in session['actors']:
            if (actor.name == name):
                a = actor
        if a == None:
            return 'Error: actor with name "%s" does not exist.' % (name)
        if (verb == 'delete'):
            session['actors'].remove(a)
        elif (verb == 'edit'):
            new_name = request.form['newName']
            for actor in session['actors']:
                if (actor.name == new_name):
                    return 'Error: actor with name "%s" already exists.' % (name)
            a.name = new_name
            name = '%s,%s' % (name, new_name)
    session.modified = True
    return '%s,' % (name)

@app.route("/goals")
def goals():
    return render_template('goals.html', actors = session['actors'])

@app.route('/goal', methods=['POST',])
def goal():
    name = request.form['name']
    parent = request.form['parent']
    verb = request.form['verb']
    actorToEdit = None
    for actor in session['actors']:
        if (actor.name == parent):
            actorToEdit = actor
    if (actorToEdit == None):
        return 'Error: actor with name "%s" does not exist.' % (parent)
    if verb == 'create':
        for goal in actorToEdit.goals:
            if (goal.name == name):
                return 'Error: goal with name "%s" already exists.' % (name)
        actorToEdit.goals.append(Goal(name))    
    elif verb == 'edit' or verb == 'delete':
        goalToEdit = None
        for goal in actorToEdit.goals:
            if (goal.name == name):
                goalToEdit = goal
        if goalToEdit == None:        
            return 'Error: goal with name "%s" does not exist.' % (name)
        if (verb == 'delete'):
            actorToEdit.goals.remove(goalToEdit)
        elif (verb == 'edit'):
            new_name = request.form['newName']
            for goal in actorToEdit.goals:
                if (goal.name == new_name):
                    return 'Error: goal with name "%s" already exists.' % (name)
            goalToEdit.name = new_name
            name = '%s,%s' % (name, new_name)
    session.modified = True
    return '%s,%s' % (name, parent)


@app.route("/data")
def data():
    return render_template('data.html', actors = session['actors'])

@app.route('/datum', methods=['POST',])
def datum():
    name = request.form['name']
    parent = request.form['parent']
    verb = request.form['verb']
    actorToEdit = None
    for actor in session['actors']:
        if (actor.name == parent):
            actorToEdit = actor
    if (actorToEdit == None):
        return 'Error: actor with name "%s" does not exist.' % (parent)
    if verb == 'create':
        for datum in actorToEdit.data:
            if (datum.name == name):
                return 'Error: datum with name "%s" already exists.' % (name)
        actorToEdit.data.append(Datum(name))    
    elif verb == 'edit' or verb == 'delete':
        datumToEdit = None
        for datum in actorToEdit.data:
            if (datum.name == name):
                datumToEdit = datum
        if datumToEdit == None:        
            return 'Error: datum with name "%s" does not exist.' % (name)
        if (verb == 'delete'):
            actorToEdit.data.remove(datumToEdit)
        elif (verb == 'edit'):
            new_name = request.form['newName']
            for datum in actorToEdit.goals:
                if (datum.name == new_name):
                    return 'Error: datum with name "%s" already exists.' % (name)
            datumToEdit.name = new_name
            name = '%s,%s' % (name, new_name)
    session.modified = True
    return '%s,%s' % (name, parent)

@app.route("/disclosures")
def disclosures():
    if (session['disclosures'] == None):
        session['disclosures'] = []
    actors = session['actors']
    possible_disclosures = main.get_possible_disclosures(actors)
    disclosures = main.trim_disclosures(session['disclosures'], possible_disclosures)
    session['disclosures'] = disclosures
    session.modified = True
    return render_template('disclosures.html', actors = actors, disclosures = disclosures)

@app.route("/disclosure", methods=['POST',])
def disclosure():
    to_actor = request.form['to_actor']
    data = request.form['data']
    from_actor = request.form['from_actor']
    flag = request.form['flag']
    disclosures = session['disclosures']
    if (flag == 'true'):
        for d in disclosures:
            if d.to_actor == to_actor and d.data == data and d.from_actor == from_actor:
                return 'Error: disclosure "%s" already flagged.' % (d)
        disclosures.append(Disclosure(from_actor, data, to_actor))
        session.modified = True
        return "Flagged %s, %s, %s" % (from_actor, data, to_actor)
    else:
        disclosureToRemove = None
        for d in disclosures:
            if d.to_actor == to_actor and d.data == data and d.from_actor == from_actor:
                disclosureToRemove = d
        if d == None:
            return 'Error: disclosure "%s" not flagged.' % (d)
        disclosures.remove(d)
        session.modified = True
        return "Unflagged %s, %s, %s" % (from_actor, data, to_actor)

@app.route("/mitigations")
def mitigations():
    if (session['mitigations'] == None):
        session['mitigations'] = []
        
    possible_disclosures = main.get_possible_disclosures(session['actors'])
    disclosures = main.trim_disclosures(session['disclosures'], possible_disclosures)
    session['disclosures'] = disclosures
    mitigations = main.trim_mitigations(session['mitigations'], disclosures)    
    session['mitigations'] = mitigations
    session.modified = True
    return render_template('mitigations.html', disclosures = disclosures, mitigations = mitigations, categories = main.mitigation_categories)

@app.route("/mitigation", methods=['POST',])
def mitigation():
    to_actor = request.form['to_actor']
    data = request.form['data']
    from_actor = request.form['from_actor']
    category = request.form['category']
    flag = request.form['flag']
    disclosures = session['disclosures']
    mitigations = session['mitigations']
    disclosureToModify = None
    for d in disclosures:
        if d.to_actor == to_actor and d.data == data and d.from_actor == from_actor:
            disclosureToModify = d
    if (disclosureToModify == None):
        return 'Error: disclosure "%s" not flagged.' % {d}
    if (flag == 'true'):
        for m in mitigations:
            if (m.disclosure == disclosureToModify and m.category == category):
                return 'Error: mitigation "%s" already flagged.' % (m)
        mitigations.append(Mitigation(disclosureToModify, category))
        session.modified = True
        return "Flagged %s, %s" % (disclosureToModify, category)
    else:
        mitigationToRemove = None
        for m in mitigations:
            if m.disclosure.from_actor == disclosureToModify.from_actor and m.disclosure.data == disclosureToModify.data and m.disclosure.to_actor == disclosureToModify.to_actor and m.category == category:
                mitigationToRemove = m
        if mitigationToRemove == None:
            return 'Error: mitigation "%s" not flagged.' % (mitigationToRemove)
        mitigations.remove(mitigationToRemove)
        session.modified = True
        return "Unflagged %s, %s" % (disclosureToModify, category)
        
@app.route("/impacts")
def impacts():
    possible_disclosures = main.get_possible_disclosures(session['actors'])
    disclosures = main.trim_disclosures(session['disclosures'], possible_disclosures)
    session['disclosures'] = disclosures
    mitigations = main.trim_mitigations(session['mitigations'], disclosures)    
    session['mitigations'] = mitigations    
    session.modified = True
    impacts = []
    return render_template('impacts.html', impacts = impacts, mitigations = mitigations, actors = session['actors'])

@app.route("/impact", methods=['POST',])
def mitigation():
    value = request.form['value']
    actor = request.form['actor']
    goal = request.form['goal']    
    to_actor = request.form['to_actor']
    data = request.form['data']
    from_actor = request.form['from_actor']
    category = request.form['category']

    mitigations = session['mitigations']
    impacts = session['impacts']
    
    mitigationToModify = None
    for m in mitigation:
        if m.to_actor == to_actor and m.data == data and m.from_actor == from_actor and m.category == category:
            mitigationToModify = m
    if (mitigationToModify == None):
        return 'Error: mitigation "%s" does not exist.' % {m}
    impactToModify = None
    for i in impacts:
        if (i.mitigation == mitigationToModify and i.goal = goal and i.actor = actor):
            impactToModify = i
    if impactToModify == None:
        impactToModify = Impact(value, actor, goal, mitigationToModify)
        impacts.append(impactToModify)
    else:
        impactToModify.value == value

    session.modified = True
    return "Modified %s, %s" % (impactToModify, value)

      
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RS'

if __name__ == "__main__":
    app.debug = True
    app.run()