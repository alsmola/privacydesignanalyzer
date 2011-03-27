from flask import Flask, render_template, request, session
from main import Actor, Goal, Datum, Group, Disclosure, Mitigation, Impact
import main

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/actors", methods=['GET',])
def actors():
    return render_template('actors.html', actors = session['actors'].items)

@app.route('/actor', methods=['POST',])
def actor():
    actors = session['actors']
    name = request.form['name']
    verb = request.form['verb']
    if verb == 'create':
        actors.add(Actor(name))
    elif (verb == 'delete'):
        actors.remove(name)
    elif (verb == 'edit'):
        new_name = request.form['newName']
        actors.update(name, new_name)
        name = '%s,%s' % (name, new_name)
    session.modified = True
    return '%s,' % (name)
    
@app.route("/goals")
def goals():
    return render_template('goals.html', actors = session['actors'].items)

@app.route('/goal', methods=['POST',])
def goal():
    name = request.form['name']
    parent = request.form['parent']
    verb = request.form['verb']
    actors = session['actors']
    actorToEdit = actors.find(parent)
    if (actorToEdit == None):
        return 'Error: actor with name "%s" does not exist.' % (parent)
    if verb == 'create':
        actorToEdit.goals.add(Goal(name))    
    elif (verb == 'delete'):
        actorToEdit.goals.remove(name)
    elif (verb == 'edit'):
        new_name = request.form['newName']
        actorToEdit.goals.update(name, new_name)
        name = '%s,%s' % (name, new_name)
    session.modified = True
    return '%s,%s' % (name, parent)


@app.route("/data")
def data():
    return render_template('data.html', actors = session['actors'].items)

@app.route('/datum', methods=['POST',])
def datum():
    name = request.form['name']
    parent = request.form['parent']
    verb = request.form['verb']
    actors = session['actors']
    actorToEdit = actors.find(parent)
    if (actorToEdit == None):
        return 'Error: actor with name "%s" does not exist.' % (parent)
    if verb == 'create':
        actorToEdit.data.add(Datum(name))    
    elif (verb == 'delete'):
        actorToEdit.data.remove(name)
    elif (verb == 'edit'):
        new_name = request.form['newName']
        actorToEdit.data.update(name, new_name)
        name = '%s,%s' % (name, new_name)
    session.modified = True
    return '%s,%s' % (name, parent)

@app.route("/disclosures")
def disclosures():
    session['disclosures'] = []
    actors = session['actors']
    possible_disclosures = main.get_possible_disclosures(actors)
    session['disclosures'] = main.trim_disclosures(session['disclosures'], possible_disclosures)
    session.modified = True
    return render_template('disclosures.html', actors = actors.items, disclosures = session['disclosures'])

@app.route("/disclosure", methods=['POST',])
def disclosure():
    to_actor_name = request.form['to_actor_name']
    data_name = request.form['data_name']
    from_actor_name = request.form['from_actor_name']
    flag = request.form['flag']
    disclosures = session['disclosures']
    d = main.find_disclosure(from_actor_name, data_name, to_actor_name,  session['actors'], disclosures)
    if (flag == 'true'):
        if (d != None): 
            return 'Error: disclosure "%s" already flagged.' % (d)
        disclosures.append(main.create_disclosure(from_actor_name, data_name, to_actor_name, session['actors']))
        session.modified = True
        return "Flagged %s, %s, %s" % (from_actor_name, data_name, to_actor_name)
    else:
        if d == None:
            return 'Error: disclosure "%s" not flagged.' % (d)
        disclosures.remove(d)
        session.modified = True
        return "Unflagged %s, %s, %s" % (from_actor_name, data_name, to_actor_name)

@app.route("/mitigations")
def mitigations():
    #if (session['mitigations'] == None):
    session['mitigations'] = []        
    possible_disclosures = main.get_possible_disclosures(session['actors'])
    session['disclosures'] = main.trim_disclosures(session['disclosures'], possible_disclosures)
    session['mitigations'] = main.trim_mitigations(session['mitigations'], session['disclosures'])
    session.modified = True
    return render_template('mitigations.html', disclosures = session['disclosures'], mitigations = session['mitigations'], categories = main.mitigation_categories)

@app.route("/mitigation", methods=['POST',])
def mitigation():
    to_actor_name = request.form['to_actor_name']
    data_name = request.form['data_name']
    from_actor_name = request.form['from_actor_name']
    category = request.form['category']
    flag = request.form['flag']
    disclosures = session['disclosures']
    mitigations = session['mitigations']
    disclosureToModify = main.find_disclosure(from_actor_name, data_name, to_actor_name)
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
            if m.disclosure == disclosureToModify and m.category == category:
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
    session['mitigations'] = main.trim_mitigations(session['mitigations'], session['disclosures'])      
    session['impacts'] = main.trim_impacts(session['impacts'], session['mitigations'], session['actors'])
    session.modified = True
    return render_template('impacts.html', impacts = session['impacts'], mitigations = session['mitigations'], actors = session['actors'].items)

@app.route("/impact", methods=['POST',])
def impact():   
    from_actor_name = request.form['from_actor_name']
    data_name = request.form['data_name']
    to_actor_name = request.form['to_actor_name']
    category = request.form['category']
    actor = request.form['actor_name']
    goal = request.form['goal']
    effect = request.form['effect']
    
    actors = session['actors']
    disclosures = session['disclosures']
    mitigations = session['mitigations']
    session['impacts'] = []
    
    d = main.find_disclosure(from_actor_name, data_name, to_actor_name, actors, disclosures)
    
    mitigationToModify = None
    for m in mitigation:
        if m.disclosure == d and m.category == category:
            mitigationToModify = m
    if (mitigationToModify == None):
        return 'Error: mitigation "%s" does not exist.' % {m}
    impactToModify = None
    for i in impacts:
        if (i.mitigation == mitigationToModify and i.goal == goal and i.actor == actor):
            impactToModify = i
    if impactToModify == None:
        impactToModify = Impact(mitigationToModify, actor, goal, effect)
        impacts.append(impactToModify)
    else:
        impactToModify.effect == effect

    session.modified = True
    return "Modified %s, %s" % (impactToModify, effect)

 
@app.route("/p2pu")
def p2pu():
    learners = Actor('Learners', Group([Goal('Learn about subjects from peer contributions'), Goal('Contribute to others\' learning by asking helpful questions and providing feedback'), Goal('Avoid revealing embarrassing or otherwise harmful information online')]), Group([Datum('Display Name'), Datum('Username'), Datum('First & last name'), Datum('Email address'), Datum('Password'), Datum('Location'), Datum('Bio'), Datum('Profile image'), Datum('Links'), Datum('RSS feeds from links'), Datum('Followers'), Datum('Follower count'), Datum('Following'), Datum('Following count'), Datum('Enrolled courses'), Datum('Private messages'), Datum('Clickstream activity')]))
    facilitators = Actor('Facilitators', Group([Goal('Organize courses that are compelling and informative'), Goal('Encourage feedback and student participation'), Goal('Avoid revealing embarrassing or otherwise harmful information online')]), Group([]))
    organizers = Actor('Organizers', Group([Goal('Create an open environment for learning'), Goal('Bring high-quality learning material to as many people who want it as possible'), Goal('Respect users by recognizing and appropriately treating sensitive information')]), Group([]))
    #developers = Actor('Developers', Group([Goal('Develop systems that are functional'), Goal('Develop systems that are usable'), Goal('Develop systems that are safe')]), Group([]))
    #research = Actor('Research community', Group([Goal('Conduct research and experiments that provide insight and guidance to academia and professional spheres'), Goal('Follow ethical guidelines')]), Group([]))
    #search = Actor('Search engines', Group([Goal('Make all information on the web easily accessible to every web user'), Goal('Follow sites directives with regards to spidering and storing information')]), Group([]))
    #public = Actor('Public', Group(['Benefit from courses without directly participating']), Group([]))
    #isp = Actor('Internet service providers', Group([Goal('Offer reliable, affordable service'), Goal('Abide by local laws and regulations')]), Group([]))
    #govt = Actor('Governments', Group([Goal('Ensure safety and security')]), Group([]))
    session['actors'] = Group([learners, facilitators, organizers])
    session['disclosures'] = []
    session['mitigations'] = []
    session['impacts'] = []
    session.modified = True
    return 'Length: %s' % (len(session['actors'].items))

@app.route("/test")
def test():
    session['objects'] = 'Think'
    session.modified = True
    return "Fuck"
    
app.secret_key = ''

if __name__ == "__main__":
    app.debug = True
    app.run()