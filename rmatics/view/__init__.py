from flask import (
    g,
    jsonify,
    session,
)
from functools import wraps
from sqlalchemy import exists, join

from rmatics.model import db
from rmatics.model.problem import EjudgeProblem
from rmatics.model.role import (
    Role,
    RoleAssignment,
)
from rmatics.model.statement import Statement
from rmatics.model.user import SimpleUser
from rmatics.utils.exceptions import (
    Forbidden,
    Unauthorized,
)


def handle_api_exception(api_exception):
    response = jsonify(api_exception.serialize())
    response.status_code = api_exception.code
    return response


def load_user():
    user_id = session.get('user_id')
    user = db.session.query(SimpleUser).filter_by(id=user_id).first()
    g.user = user


def load_problem(problem_id):
    problem = db.session.query(EjudgeProblem).filter_by(id=problem_id).first()
    g.problem = problem


def load_statement(statement_id):
    statement = db.session.query(Statement).filter_by(id=statement_id).first()
    g.statement = statement


def require_auth(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not g.get('user', None):
            raise Unauthorized
        return func(*args, **kwargs)
    return wrapped


def require_roles(*roles):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not getattr(g, 'user', None):
                raise Unauthorized

            role_assignment_exists = db.session.query(
                exists() \
                    .select_from(join(RoleAssignment, Role)) \
                    .where(RoleAssignment.user_id == g.user.id) \
                    .where(Role.shortname.in_(roles))
            ).scalar()

            if not role_assignment_exists:
                raise Forbidden

            return func(*args, **kwargs)
        return wrapped
    return wrapper


# @current_app.before_request
# def load_problem():
#     print('load problem')
#     for l in vars(request).keys():
#         print(l)
#     print(request.view_args)
#     print(request.args)
