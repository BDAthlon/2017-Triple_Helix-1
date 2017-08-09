from flask import Blueprint, redirect, render_template, url_for

from glyphrepository.glyph.models import Glyph
from glyphrepository.soterm.models import SOterm

blueprint = Blueprint('sboterm', __name__, static_folder='../static', url_prefix='/sboterm',)

@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """No SBO term specified so edirect home."""
    return redirect(url_for('public.home'))

@blueprint.route('/<sboterm_id>', methods=['GET', 'POST'])
def list_so_glyphs(soterm_id):
    """List all glyphs matching this SBO term."""
    soterm_id = soterm_id.replace('SO:', '')
    glyphs = Glyph.query.filter_by(soterm_id=soterm_id).all()
    soterm = SOterm.query.filter_by(id=soterm_id).first()

    return render_template('soterm/soterm.html', glyphs=glyphs, soterm=soterm)

