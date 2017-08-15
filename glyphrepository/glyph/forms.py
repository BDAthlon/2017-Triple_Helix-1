# -*- coding: utf-8 -*-
"""Glyph forms."""
from flask_wtf import Form
from wtforms import StringField, FileField, SelectField
from wtforms.validators import DataRequired


class AddGlyphForm(Form):
    """Form to add a new glyph."""

    name = StringField('Glyph name', validators=[DataRequired()])
    soTerm = SelectField('SO term', choices=[])
    sbol_status = SelectField('Status in SBOLv standard process',
                              choices=map(lambda x: (x, x),['Proposed', 'Endorsed', 'Adopted (recommended)', 'Adopted (alternative)']))
    proposal_url = StringField('URL of proposal google doc')

    file_path = FileField()

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(AddGlyphForm, self).__init__(*args, **kwargs)

    def validate(self):
        """Validate the form."""
        return super(AddGlyphForm, self).validate()
