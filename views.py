from flask import render_template, \
        request, \
        redirect, \
        url_for, \
        flash, \
        current_app, \
        session, \
        Blueprint

from flask_security.core import current_user
from flask_security.decorators import login_required, roles_required
from flask.ext.classy import FlaskView, route
from werkzeug.utils import import_string
from wtforms.ext.sqlalchemy.orm import model_form
from willow.models import db, Chapter, Venue, Role, User
from willow.forms import WLWForm, NewChapterForm, NewVenueForm, NewRoleForm
from willow.blueprints.admin import ModelAdminView
from utplugin.models import Subscription

import os

template_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'templates'))
ut_blueprint = Blueprint('utplugin', __name__, template_folder=template_path)

class AdminSubscriptionView(ModelAdminView):
    route_base="/subs"
    wlw_model = Subscription
    wlw_title = 'Subscription'
    wlw_key = 'subs'

    def get_form(self, **kwargs):
        pass

    def get_new_view_name(self):
        return "%s:index" % (self.view_base(),)

    def view_base(self):
        return "utplugin.AdminSubscriptionView"

class AdminUserListView(ModelAdminView):
    route_base="/users"
    wlw_model = User
    wlw_title = 'UT User'
    wlw_key = 'users'
    template = 'admin/wlw_admin_list_index.html'

    def get_template(self, action=None):
        return self.template

    @route('/')
    def index(self):
        objects = User.query.filter_by(active=True).all()
        return render_template(self.get_template(),
                objects=objects,
                obj_type=self.wlw_key,
                new_url='',
                model_title=self.wlw_title,
                secondary="")

AdminUserListView.register(ut_blueprint)
AdminSubscriptionView.register(ut_blueprint)
