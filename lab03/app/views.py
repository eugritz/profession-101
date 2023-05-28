from . import app
from . import schemas
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    figures = [
        schemas.TetrahedronSchema,
        schemas.HexahedronSchema,
        schemas.OctahedronSchema,
        schemas.DodecahedronSchema,
        schemas.IcosahedronSchema
    ]
    return render_template('index.html', figures=figures)
