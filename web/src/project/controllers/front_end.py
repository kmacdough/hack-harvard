from flask import render_template, jsonify

from .. import app


@app.route('/startgame', methods=['GET'])
def hello():
    # jinja2 templates
    return render_template('hello.html', name="noname")
