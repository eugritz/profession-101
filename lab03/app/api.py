from .schemas import FIGURES
from .figures import CalculationError
from flask import Blueprint, make_response, request
from marshmallow import ValidationError


api = Blueprint('api', __name__)


def api_success(data):
    return make_response({ 'data': data, 'errors': None }, 200)


def api_error(message):
    return make_response({ 'data': None, 'errors': message }, 400)


@api.route('/api/calculate/<string:id>', methods=['POST'])
def calculate(id: str):
    figure = next(filter(lambda x: x.id == id, FIGURES), None)
    if not figure:
        return api_error('Invalid figure')

    try:
        schema = figure()
        figure = schema.load(request.get_json(force=True))
        return api_success(schema.dump(figure))
    except CalculationError as e:
        return api_error(str(e))
    except ValidationError as e:
        return api_error(e.messages)
