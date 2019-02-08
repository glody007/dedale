from functools import wraps
from flask import abort
from flask_login import current_user
from utils import Permission

def permission_requise(permission):
    def decorateur(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.peut(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorateur

def guru_requis(f):
    return permission_requise(Permission.SUPPRIMER_ECOLE)(f)

def moine_requis(f):
    return permission_requise(Permission.MODIFIER_ECOLE)(f)
