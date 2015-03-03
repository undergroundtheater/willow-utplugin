from willow.models import db
from willow.models.user import Role, User
from flask import Blueprint
from .views import ut_blueprint, AdminSubscriptionView

class UTPlugin(object):
    has_models = True
    model_names = [
            'utplugin.models.UTProfile',
            'utplugin.models.Subscription',
            ]

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.register_blueprint(ut_blueprint, url_prefix='/ut')
        app.navbar['admin'].insert(0,
                (
                    '',
                    'UT Users',
                    'utplugin.AdminUserListView:index',
                    ))
        app.navbar['admin'].append(
                (
                    '',
                    'Patronages',
                    'utplugin.AdminSubscriptionView:index',
                    )
            )

        if getattr(app, 'init_db_hooks', False):
            app.init_db_hooks.append(self.__class__.init_db)
        else:
            app.init_db_hooks = [self.__class__.init_db]

    @staticmethod
    def init_db(app, db):
        try:
            role = Role(name="UT Administrator", description="UT Admin")
            db.session.add(role)
            db.session.commit()
        except:
            db.session.rollback()
            role = Role.query.filter_by(name='UT Administrator')

        user = User.query.get(1)
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()

        if user.ut_subscriptions.count() == 0:
            from datetime import datetime, timedelta
            from pytz import UTC
            from utplugin.models import Subscription
            datenow = datetime.now(UTC)
            dateexpire = datenow + timedelta(days=365)
            sub = Subscription(user=user,
                    name=user.wlw_profile.name,
                    dateactive=datenow,
                    dateexpiry=dateexpire)
            db.session.add(sub)
            db.session.commit()

