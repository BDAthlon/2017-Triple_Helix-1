from flask import Blueprint, redirect, render_template, url_for

from glyphrepository.glyph.models import Glyph
from glyphrepository.sboterm.models import SBOterm

blueprint = Blueprint('sboterm', __name__, static_folder='../static', url_prefix='/sboterm',)

@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """No SBO term specified so edirect home."""
    return redirect(url_for('public.home'))

@blueprint.route('/<sboterm_id>', methods=['GET', 'POST'])
def list_sbo_glyphs(sboterm_id):
    """List all glyphs matching this SBO term."""
    sboterm_id = sboterm_id.replace('SBO:', '')
    glyphs = Glyph.query.filter_by(sboterm_id=sboterm_id).all()
    sboterm = SBOterm.query.filter_by(id=sboterm_id).first()

    return render_template('sboterm/sboterm.html', glyphs=glyphs, sboterm=sboterm)

