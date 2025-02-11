#!/usr/bin/python3
"""
A script that starts a Flask web application:listening on 0.0.0.0, port 5000
"""

from flask import Flask
from models import storage
from flask import render_template

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states_list_route():
    """
    List states: display a HTML page: (inside the tag BODY)
    Returns:
        html: template that lists all states sort by name A->Z
    """
    states = storage.all("State").values()
    return render_template("7-states_list.html", states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_by_id_route(id):
    """
    Get a state by id
    Returns:
        html: template that lists cities of state sort by name A->Z
    """
    state = None
    for s in storage.all("State").values():
        if s.id == id:
            state = s
            break
    return render_template("9-states.html", state=state)


@app.teardown_appcontext
def close_db(exception=None):
    """
    After each request remove the current SQLAlchemy Session:
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
