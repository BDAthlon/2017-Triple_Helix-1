# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from flask_github import GitHub
from flask import current_app as app

from glyphrepository.extensions import login_manager
from glyphrepository.public.forms import LoginForm
from glyphrepository.user.forms import RegisterForm
from glyphrepository.user.models import User
from glyphrepository.utils import flash_errors

from glyphrepository.glyph.models import Glyph
import requests
import json

blueprint = Blueprint('public', __name__, static_folder='../static')

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('public.home')
            return redirect(redirect_url)
        else:
            flash_errors(form)

    return render_template('public/home.html', glyphs=Glyph.query.order_by(Glyph.soterm_id.asc()).all())


@blueprint.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('public/login.html', form=form)


@blueprint.route('/github-login')
def github_login():
    github = GitHub(app)
    if not current_user.is_authenticated:
        return github.authorize(scope="user")
    else:
        flash('You are already logged in.', 'success')
        return redirect(url_for('public.home'))


@blueprint.route('/github-callback')
def authorized():
    github = GitHub(app)
    if 'code' in request.args:
        access_token = github._handle_response()
    else:
        access_token = github._handle_invalid_response()

    if not access_token:
        flash('Error getting access token.', 'warning')
        return redirect(url_for('public.home'))

    r = requests.get('https://api.github.com/user', params={"access_token": access_token})
    user_details = json.loads(r.content)

    if not user_details:
        flash('Error getting user details.', 'warning')
        return redirect(url_for('public.home'))

    # if necessary, add user
    github_username = user_details["login"]

    email = user_details["email"]
    if not email:
        email = github_username

    user = User.query.filter_by(github_username=github_username).first()

    if user:
        login_user(user)
        flash('You have logged-in using GitHub.', 'success')

    if not user:
        user = User.create(username=github_username, email=email, github_username=github_username)
        login_user(user)
        flash('You have logged-in using GitHub for the first time.', 'success')

    return redirect(url_for('public.home'))


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(username=form.username.data, email=form.email.data, password=form.password.data, active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)
