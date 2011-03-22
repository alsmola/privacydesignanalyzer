from flask import Flask, render_template, request, session
import main
from main import Actor, Goal, Datum, Disclosure
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


      
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RS'

if __name__ == "__main__":
    app.debug = True
    app.run()