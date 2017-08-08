# -*- coding: utf-8 -*-
"""Section for viewing/editing a part."""
from flask import Blueprint, redirect, render_template, url_for, request, flash
from glyphrepository.utils import flash_errors

from glyphrepository.glyph.models import Glyph
from glyphrepository.glyph.forms import AddGlyphForm

from flask_login import login_required, current_user
from glyphrepository.user.models import User

blueprint = Blueprint('glyph', __name__, static_folder='../static', url_prefix='/glyph',)


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """ If no part id specified, redirect home """
    return redirect(url_for('public.home'))

@blueprint.route('/<glyph_id>', methods=['GET', 'POST'])
def show_glyph(glyph_id):
    """Show details of glyph (if it exists) or redirect home."""

    glyph_list = Glyph.query.filter(Glyph.id == glyph_id).all()

    if len(glyph_list) == 0:
        return redirect(url_for('public.home'))
    else:
        return render_template('glyph/view.html', glyph=glyph_list[0])


@blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def register():
    """Register new user."""
    form = AddGlyphForm(request.form)

    print form.validate_on_submit()

    if form.validate_on_submit():
        new_glyph = Glyph.create(name=form.name.data, file_name=form.file_path.data, sbo_term=form.sboTerm.data,  user_id = current_user.id)

        flash('Glyph successfully added.', 'success')
        return redirect(url_for('glyph.show_glyph', glyph_id=new_glyph.id))
    else:
        flash_errors(form)
    return render_template('glyph/add-glyph.html', form=form)


