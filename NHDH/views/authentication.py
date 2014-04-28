from flask import Blueprint, render_template, session, redirect, url_for, \
        request, flash, g, jsonify, abort, current_app
from flask.ext.principal import identity_changed, identity_loaded, Identity, \
        AnonymousIdentity, RoleNeed


from NHDH import app
from NHDH.database import db_session
from NHDH.models.user import User, roles

# This blueprint does not provide url prefix!
mod = Blueprint('authentication', __name__)

@mod.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(url_for('profile.view'))

    if 'cancel' in request.form:
        flash(u'Cancelled. The OpenID was not changed.')
        return redirect(oid.get_next_url())

    openid = request.values.get('openid')

    if not openid:
        openid = COMMON_PROVIDERS.get(request.args.get('provider'))

    if openid:
        return oid.try_login(openid, ask_for=['fullname', 'email', 'language'])

    error = oid.fetch_error()
    if error:
        flash(u'Error: ' + error)

    return render_template('authentication/login.html', next=oid.get_next_url())

@mod.route('/logout')
def logout():
    if 'user' in session:
        identity_changed.send(
            current_app._get_current_object(),
            identity = AnonymousIdentity()
        )
        for key in ('user', 'openid', 'identity.name', 'identity.auth_type'):
            session.pop(key, None)
        flash(u'Logged out')

    return redirect(url_for('home.index'))


@oid.after_login
def create_or_login(response):
    '''
    This is the hook for OpenID.try_login and is being called after a response
    has been received.
    '''

    session['user'] = {}
    session['openid'] = response.identity_url

    user = g.user or User.query.filter_by(openid=response.identity_url).first()

    if user is None:
        name = response.fullname or response.nickname
        session['user']['email'] = response.email
        params = dict(next=oid.get_next_url(), name = name)
        return redirect(url_for('.first_login', **params))

    g.user = user
    identity = Identity(user.id)

    # Notify Principal of the identity change
    identity_changed.send(
        current_app._get_current_object(),
        identity = identity
    )

    if user.openid != response.identity_url:
        user.openid = response.identity_url
        db_session.commit()
        flash(u'OpenID identity changed')
    else:
        flash(u'Successfully signed in', 'hurray')

    return redirect(oid.get_next_url())

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    user = User.query.filter_by(id=identity.name).first()
    if not user:
        return
    load_identity(identity, user)

@identity_changed.connect_via(app)
def on_identity_changed(sender, identity):
    if not g.user:
        return
    load_identity(identity, g.user)


def load_identity(identity, user):
    '''
    Handles loading the user identity
    '''

    identity.provides.add(RoleNeed("user"))

    if not user.active or not user.verified:
        return

    if not user.role:
        return

    keys = roles.keys()
    top = max(keys)
    identity.provides.add(RoleNeed(roles.get(user.role)))

    for k in keys:
        if k > user.role:
            role = roles.get(k, None)
            identity.provides.add(RoleNeed(roles.get(k)))