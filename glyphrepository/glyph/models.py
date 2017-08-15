# -*- coding: utf-8 -*-
"""Glyph models."""
from __future__ import division

from glyphrepository.database import Column, Model, SurrogatePK, db, reference_col, relationship

class Glyph(SurrogatePK, Model):
    """A glyph."""

    __tablename__ = 'glyphs'
    name = Column(db.String(80), unique=False, nullable=False)
    file_name = Column(db.String(80), unique=False, nullable=False)

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