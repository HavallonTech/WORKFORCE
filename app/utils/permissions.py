from functools import wraps

from flask import abort

from flask_login import current_user


def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if current_user.role not in [
            "admin",
            "superadmin"
        ]:

            abort(403)

        return f(*args, **kwargs)

    return decorated_function


def superadmin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if current_user.role != "superadmin":

            abort(403)

        return f(*args, **kwargs)

    return decorated_function