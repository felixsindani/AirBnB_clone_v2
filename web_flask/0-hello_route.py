#!/usr/bin/python3
"""
A script that starts a Flask web application:
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_route():
    """
    Displays 'Hello HBNB!'
    Returns:
        str: "Hello HBNB"
    """
    return render_template("100-hbnb.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port= 5000, debug=None)
