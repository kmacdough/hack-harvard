from .. import app
from flask import render_template

@app.route('/', methods=['GET'])
def hello():
    return render_template('hello.html', name="noname")
