from passlib.hash import bcrypt
from flask import current_app, flash, abort
from flask_security.core import current_user
from willow.app import willow_signals, is_admin
from willow.models import db
from willow.models.mixins import WLWMixin
from flask.ext.security import RoleMixin, UserMixin
from sqlalchemy import and_, or_
from sqlalchemy.ext.declarative import declared_attr

class UTProfile(db.Model):
    __tablename__ = 'ut_profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', 
            primaryjoin="foreign(UTProfile.user_id) == User.id",
            uselist=False,
            cascade=False,
            lazy='joined',
            backref=db.backref('wlw_profile', uselist=False, lazy='joined'))
    name = db.Column(db.String)
    patron_id = db.Column(db.Integer, nullable=True)
    primary_chapter_id = db.Column(db.Integer, nullable=True)
    primary_chapter = db.relationship('Chapter',
            primaryjoin='foreign(UTProfile.primary_chapter_id) == Chapter.id',
            uselist=False,
            cascade=False,
            lazy='joined')

    def is_active(self):
        return self.user.is_active()

    def is_admin(self):
        return self.has_role('admin')

    def has_role(self, rolename):
        # TODO: for testing
        return True

    def is_patron(self):
        from datetime import datetime
        from pytz import UTC
        utcnow = datetime.now(UTC)
        if getattr(self.user, 'ut_subscriptions', False):
            subs = self.user.ut_subscriptions.filter(
                    and_(Subscription.dateactive <= utcnow, Subscription.dateexpiry > utcnow, Subscription.active == True)
                    )

        return False

class Subscription(db.Model, WLWMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', 
            primaryjoin="foreign(Subscription.user_id) == User.id",
            uselist=False,
            cascade=False,
            lazy='joined',
            backref=db.backref('ut_subscriptions', uselist=True, lazy='dynamic'))
    patron_id = db.Column(db.Integer, nullable=True)
    dateactive = db.Column(db.DateTime(timezone=True),
            default=db.func.now())
    dateexpiry = db.Column(db.DateTime(timezone=True))

    @declared_attr
    def __tablename__(cls):
        return 'ut_patronage'
