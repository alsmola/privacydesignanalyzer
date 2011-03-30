from flask import Flask, render_template, request, session, jsonify
from main import Application, Actor, Goal, Datum, Disclosure, Mitigation, Impact, db
from flaskext.sqlalchemy import SQLAlchemy
import main

app = Flask(__name__)
app_id = 1

@app.route("/")
def start():
    return render_template('start.html', apps = Application.query.all())

@app.route("/actors", methods=['GET',])
def actors():
    app_id = request.args['app_id']
    return render_template('actors.html', actors = Actor.query.filter_by(app_id=app_id).all(), app_id=app_id)

@app.route('/actor', methods=['POST',])
def actor():
    id = request.form['id']
    parent_id = request.form['parent_id']
    name = request.form['name']
    verb = request.form['verb']
    if verb == 'create':
        actor = Actor(name, parent_id)
        db.session.add(actor)
    else:
        actor = Actor.query.filter_by(id=id).first()
        if (verb == 'delete'):    
            db.session.delete(actor)
        elif (verb == 'edit'):
            new_name = request.form['newName']
            actor.name = new_name
            name = new_name
    db.session.commit()
    id = actor.id
    return jsonify(id=id, name=name, verb=verb, parent_id=parent_id, success = True, type = 'actor', parent_type = 'app')
    
@app.route("/goals")
def goals():
    actors = Actor.query.filter_by(app_id=app_id).all()
    return render_template('goals.html', actors = Actor.query.filter_by(app_id=app_id).all())

@app.route('/goal', methods=['POST',])
def goal():
    id = request.form['id']
    parent_id = request.form['parent_id']
    name = request.form['name']
    verb = request.form['verb']
    if verb == 'create':
        goal = Goal(name, parent_id)
        db.session.add(goal)
    else:
        goal = Goal.query.filter_by(id=id).first()
        if (verb == 'delete'):    
            db.session.delete(goal)
        elif (verb == 'edit'):
            new_name = request.form['newName']
            goal.name = new_name
            name = new_name
    db.session.commit()
    id = goal.id
    return jsonify(id=id, name=name, verb=verb, parent_id=parent_id, success = True, type = 'goal', parent_type = 'actor')


@app.route("/data")
def data():
    return render_template('data.html', actors = Actor.query.filter_by(app_id=app_id).all())

@app.route('/datum', methods=['POST',])
def datum():
    id = request.form['id']
    parent_id = request.form['parent_id']
    name = request.form['name']
    verb = request.form['verb']
    if verb == 'create':
        datum = Datum(name, parent_id)
        db.session.add(datum)
    else:
        datum = Datum.query.filter_by(id=id).first()
        if (verb == 'delete'):    
            db.session.delete(datum)
        elif (verb == 'edit'):
            new_name = request.form['newName']
            datum.name = new_name
            name = new_name
    db.session.commit()
    id = datum.id
    return jsonify(id=id, name=name, verb=verb, parent_id=parent_id, success = True, type = 'datum', parent_type = 'actor')

@app.route("/disclosures")
def disclosures():
    return render_template('disclosures.html', actors = Actor.query.filter_by(app_id=app_id).all(), disclosures = Disclosure.query.filter_by(app_id=app_id).all(), app_id = app_id)

@app.route("/disclosure", methods=['POST',])
def disclosure():
    app_id = request.form['app_id']
    from_actor_id = request.form['from_actor_id']
    datum_id = request.form['datum_id']
    to_actor_id = request.form['to_actor_id']
    flagged = request.form['flagged']
    if flagged == 'true':
        disclosure = Disclosure(app_id, from_actor_id, datum_id, to_actor_id)
        db.session.add(disclosure)
    else:
        disclosure = Disclosure.query.filter_by(from_actor_id=from_actor_id,datum_id=datum_id,to_actor_id=to_actor_id).first()
        db.session.delete(disclosure)
    db.session.commit()
    id = disclosure.id
    return jsonify(id=id, success = True)

@app.route("/mitigations")
def mitigations():
    return render_template('mitigations.html', disclosures = Disclosure.query.filter_by(app_id=app_id).all(), mitigations = Mitigation.query.filter_by(app_id=app_id).all(), categories=main.categories, app_id = app_id)

@app.route("/mitigation", methods=['POST',])
def mitigation():
    app_id = request.form['app_id']
    disclosure_id = request.form['disclosure_id']
    category = request.form['category']
    flagged = request.form['flagged']
    if flagged == 'true':
        mitigation = Mitigation(app_id, disclosure_id, category)
        db.session.add(mitigation)
    else:
        mitigation = Mitigation.query.filter_by(disclosure_id=disclosure_id,category=category).first()
        db.session.delete(mitigation)
    db.session.commit()
    id = mitigation.id
    return jsonify(id=id, success = True)
        
@app.route("/impacts")
def impacts():
    return render_template('impacts.html', impacts = Impact.query.filter_by(app_id=app_id).all(), mitigations = Mitigation.query.filter_by(app_id=app_id).all(), actors = Actor.query.filter_by(app_id=app_id).all(), app_id = app_id)

@app.route("/impact", methods=['POST',])
def impact():   
    app_id = request.form['app_id']
    mitigation_id = request.form['mitigation_id']
    goal_id = request.form['goal_id']
    effect = request.form['effect']
    impact = Impact.query.filter_by(mitigation_id=mitigation_id,goal_id=goal_id).first()
    if impact == None:
        impact = Impact(app_id, mitigation_id, goal_id, effect)
        db.session.add(impact)
    else:
        impact.effect = effect
    db.session.commit()
    id = impact.id
    return jsonify(id=id, success = True)

@app.route("/result")
def result():
    return render_template('result.html')

@app.route("/reset")
def reset():   
    db.drop_all()
    db.create_all()
    return "Success"

@app.route("/test")
def test():
    this_app = Application('Test App')
    db.session.add(this_app)
    db.session.commit()
    
    actorGoals = { 'Users' : ['Communicate online', 'Protect privacy'], 'Developers' : ['Develop systems that are functional', 'Develop systems that are usable', 'Develop systems that are safe'], 'Search engines' : ['Make all information on the web easily accessible to every web user', 'Follow sites directives with regards to spidering and storing information'], 'Public' : ['Find useful information online'], 'Internet service providers' : ['Offer reliable, affordable service', 'Abide by local laws and regulations'], 'Governments' : ['Ensure safety and security'] }    
    actorData = { 'Users' : [ 'Username', 'First & last name', 'Email address', 'Password', 'Private messages', 'Clickstream activity'] }
    users = Actor('Users', this_app.id)
    developers = Actor('Developers', this_app.id)
    search = Actor('Search engines', this_app.id)
    public = Actor('Public', this_app.id)
    isp = Actor('Internet service providers', this_app.id)
    govt = Actor('Governments', this_app.id)
    actors = [users, developers, search, public, isp, govt]
    for actor in actors:
        db.session.add(actor)
        db.session.commit()
        if actor.name in actorGoals:
            for goal in actorGoals[actor.name]:
                db.session.add(Goal(goal, actor.id))
        if actor.name in actorData:
            for datum in actorData[actor.name]:
                db.session.add(Datum(datum, actor.id))
        db.session.commit()
    return "Success"
    
app.secret_key = ''

if __name__ == "__main__":
    app.debug = True
    app.run()