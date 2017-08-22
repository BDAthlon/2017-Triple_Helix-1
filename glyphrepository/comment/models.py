# -*- coding: utf-8 -*-
"""Comment models."""

from glyphrepository.database import Column, Model, SurrogatePK, db, reference_col, relationship

class Comment(SurrogatePK, Model):
    """A comment."""

    __tablename__ = 'comments'
    name = Column(db.String(80), unique=False, nullable=False)
    rating = Column(db.Integer, unique=False, nullable=False)
    comment = Column(db.String, unique=False, nullable=True)

    glyph_id = reference_col('glyphs', nullable=True)
    glyph = relationship('Glyph', backref='comments')

    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='comments')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)

    def get_display_rating(self):
        ratings = {"-1": "not rated", "1": "rated 1/5", "2": "rated 2/5", "3": "rated 3/5", "4": "rated 4/5",
                   "5": "rated 5/5"}
        return ratings[str(self.rating)]
