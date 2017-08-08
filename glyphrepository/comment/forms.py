# -*- coding: utf-8 -*-
"""Comment forms."""
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(Form):
    """Form to add a new glyph."""

    name = StringField('Title', validators=[DataRequired()])

    options = []
    for i in range(0, 5):
        options.append((str(i), str(i)))

    rating = SelectField('Rating', choices=options)

    comment = TextAreaField('Comment', validators=[])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(CommentForm, self).__init__(*args, **kwargs)

    def validate(self):
        """Validate the form."""
        return super(CommentForm, self).validate()
