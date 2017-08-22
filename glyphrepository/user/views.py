# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from glyphrepository.user.models import User
from glyphrepository.glyph.models import Glyph

blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@blueprint.route('/')
@login_required
def members():
    """If no user specified, redirect to homepage."""
    return redirect(url_for('public.home'))


@blueprint.route('/<user_id>')
def user(user_id):
    """Show all Glyphs by a single user."""

    user = User.query.filter(User.id == user_id).all()[0]
    glyphs = Glyph.query.filter(Glyph.user_id == user_id).order_by(Glyph.soterm_id.asc()).all()

    return render_template('user/user.html', user=user, glyphs=glyphs)