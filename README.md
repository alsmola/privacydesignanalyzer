This is a prototype tool for privacy design analysis and privacy requirements gathering. This tool will guide the user through an analysis and provide an outline of the potential privacy problems of the system as well as design alternatives that could support increased user privacy.

The goal of this tool is to help users quickly and comprehensively think about privacy issues that may affect their system and how they can be addressed with a set of privacy-preserving design choices.

It is built with [Flask](http://flask.pocoo.org/) and [FlaskSQLAlchemy](http://packages.python.org/Flask-SQLAlchemy/) running on Sqlite. You'll need to make sure these are installed.

To run, simply type:

    python front.py

and browse to <http://localhost:5000>.

You'll need to generate a test app - there is a method at <http://localhost:5000/test> to do this for you. Visit <http://localhost:5000/reset> to clear the database.

To test the app, run the unit test:

    python unittests.py
