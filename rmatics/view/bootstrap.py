from flask import (
    g,
    jsonify,
    Blueprint,
)

from rmatics.model import db


bootstrap = Blueprint('bootstrap', __name__, url_prefix='/bootstrap')


@bootstrap.route('/')
def bootstrap_get():
    serialized = {}
    if g.user:
        serialized['user'] = g.user.serialize()
    return jsonify(serialized)
