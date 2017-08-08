# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import Form
from wtforms import StringField, FileField
from wtforms.validators import DataRequired


class AddGlyphForm(Form):
    """Form to add a new glyph."""

    name = StringField('Title', validators=[DataRequired()])
    sboTerm = StringField('SBO term')
    file_path = FileField()


    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(AddGlyphForm, self).__init__(*args, **kwargs)

    def validate(self):
        """Validate the form."""
        return super(AddGlyphForm, self).validate()
