from flask import Flask, render_template, request, session
from main import Actor, Goal, Datum
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

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RS'

if __name__ == "__main__":
    app.debug = True
    app.run()