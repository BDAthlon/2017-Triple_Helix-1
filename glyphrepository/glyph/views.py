# -*- coding: utf-8 -*-
"""Section for viewing/editing a part."""
from flask import Blueprint, redirect, render_template, url_for

from glyphrepository.glyph.models import Glyph

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


# TODO: form to add Glyph

