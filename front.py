from flask import Flask, render_template, request, session, jsonify
from main import Application, Actor, Goal, Datum, Disclosure, Mitigation, Impact, db
from flaskext.sqlalchemy import SQLAlchemy
import main

app = Flask(__name__)
app_id = 1

@app.route("/")
def start():
    if len(Application.query.all()) < 1:
        this_app = Application('Test App')
        db.session.add(this_app)
        db.session.commit()
    else:
        this_app = Application.query.limit(1).first()
    return render_template('start.html', app_id = this_app.id)

@app.route("/actors", methods=['GET',])
def actors():
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
    return render_template('disclosures.html', disclosures = session['disclosures'])

@app.route("/disclosure", methods=['POST',])
def disclosure():
    pass

@app.route("/mitigations")
def mitigations():
    return render_template('mitigations.html', disclosures = session['disclosures'], mitigations = session['mitigations'])

@app.route("/mitigation", methods=['POST',])
def mitigation():
    pass
        
@app.route("/impacts")
def impacts():

    return render_template('impacts.html', impacts = session['impacts'], mitigations = session['mitigations'])

@app.route("/impact", methods=['POST',])
def impact():   

    return "Modified %s, %s" % (impactToModify, effect)

 
@app.route("/p2pu")
def p2pu():
#    learners = Actor('Learners', Group([Goal('Learn about subjects from peer contributions'), Goal('Contribute to others\' learning by asking helpful questions and providing feedback'), Goal('Avoid revealing embarrassing or otherwise harmful information online')]), Group([Datum('Display Name'), Datum('Username'), Datum('First & last name'), Datum('Email address'), Datum('Password'), Datum('Location'), Datum('Bio'), Datum('Profile image'), Datum('Links'), Datum('RSS feeds from links'), Datum('Followers'), Datum('Follower count'), Datum('Following'), Datum('Following count'), Datum('Enrolled courses'), Datum('Private messages'), Datum('Clickstream activity')]))
#    facilitators = Actor('Facilitators', Group([Goal('Organize courses that are compelling and informative'), Goal('Encourage feedback and student participation'), Goal('Avoid revealing embarrassing or otherwise harmful information online')]), Group([]))
#    organizers = Actor('Organizers', Group([Goal('Create an open environment for learning'), Goal('Bring high-quality learning material to as many people who want it as possible'), Goal('Respect users by recognizing and appropriately treating sensitive information')]), Group([]))
#    developers = Actor('Developers', Group([Goal('Develop systems that are functional'), Goal('Develop systems that are usable'), Goal('Develop systems that are safe')]), Group([]))
#    research = Actor('Research community', Group([Goal('Conduct research and experiments that provide insight and guidance to academia and professional spheres'), Goal('Follow ethical guidelines')]), Group([]))
#    search = Actor('Search engines', Group([Goal('Make all information on the web easily accessible to every web user'), Goal('Follow sites directives with regards to spidering and storing information')]), Group([]))
#    public = Actor('Public', Group(['Benefit from courses without directly participating']), Group([]))
#    isp = Actor('Internet service providers', Group([Goal('Offer reliable, affordable service'), Goal('Abide by local laws and regulations')]), Group([]))
#    govt = Actor('Governments', Group([Goal('Ensure safety and security')]), Group([]))
#    main.get_actors() = Group([learners, facilitators, organizers, developers, research, search, public, isp, govt])
#    session['disclosures'] = []
#    session['mitigations'] = []
#    session['impacts'] = []
#    session.modified = True
    return 'Length: %s' % (len(main.get_actors()))

    
app.secret_key = ''

if __name__ == "__main__":
    app.debug = True
    app.run()