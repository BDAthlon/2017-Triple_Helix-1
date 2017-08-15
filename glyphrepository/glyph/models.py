# -*- coding: utf-8 -*-
"""Glyph models."""
from __future__ import division

from glyphrepository.database import Column, Model, SurrogatePK, db, reference_col, relationship

class Glyph(SurrogatePK, Model):
    """A glyph."""

    __tablename__ = 'glyphs'
    name = Column(db.String(80), unique=False, nullable=False)
    file_name = Column(db.String(80), unique=False, nullable=False)

    has_pdf = Column(db.Boolean)
    has_png = Column(db.Boolean)
    has_svg = Column(db.Boolean)
    has_jpg = Column(db.Boolean)

    sbol_status = Column(db.String(80), unique=False, nullable=True)
    proposal_url = Column(db.String(80), unique=False, nullable=True)

    soterm_id = reference_col('soterms', nullable=True)
    soterm = relationship('SOterm', backref='glyphs')

    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='glyphs')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)

    def average_rating(self):
        """Return the average rating for a glyph, rounded to one decimal place"""

        # Make a list of all ratings >= 0 (-1 is a sentinel value for unrated)
        ratings = []
        for comment in self.comments:
            if comment.rating >= 0: 
                ratings.append(comment.rating)

        if len(ratings) == 0:
            return ""
        else:
            return "%.1f" % (sum(ratings) / len(ratings))

    def get_soterm_link(self):
        if self.soterm:
            full_id = self.soterm.get_full_id()
            return '<a href="/soterm/%s"> %s (%s)</a>' % (full_id, self.soterm.name, full_id)
        else:
            return ""

    def record_file(self, file_extension):
        if file_extension[0] == ".":
            file_extension = file_extension[1:]

        if file_extension == "pdf":
            self.has_pdf = True
        elif file_extension == "png":
            self.has_png = True
        elif file_extension == "svg":
            self.has_svg = True
        elif file_extension == "jpg":
            self.has_jpg = True

        self.save()

    def get_preferred_filename(self):
        if self.has_png:
            return str(self.id) + ".png"
        elif self.has_svg:
            return str(self.id) + ".svg"
        elif self.has_jpg:
            return str(self.id) + ".jpg"
        elif self.has_pdf:
            return str(self.id) + ".pdf"
        else:
            return ""