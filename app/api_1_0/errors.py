from . import api
from ..exceptions import ValidationError

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])

def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response
