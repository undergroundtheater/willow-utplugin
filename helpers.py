from functools import wraps
from flask import current_app, Response, request, redirect, _request_ctx_stack
from flask.ext.login import current_user
from werkzeug.local import LocalProxy

_utplugin = LocalProxy(lambda: current_app.loaded_plugins['utplugin.UTPlugin'])

def needs_profile():
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if request.user.is_authenticated():
                if user.ut_profile is not None:
                    return fn(*args, **kwargs)

            return redirect('/ut/profile/new')
