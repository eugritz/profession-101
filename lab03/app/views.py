from . import app
from .schemas import FIGURES
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', figures=FIGURES)
