# -*- coding: utf-8 -*-
"""Comment models."""

from glyphrepository.database import Column, Model, SurrogatePK, db, reference_col, relationship

class Comment(SurrogatePK, Model):
    """A comment."""

    __tablename__ = 'comments'
    name = Column(db.String(80), unique=False, nullable=False)
    rating = Column(db.Integer, unique=False, nullable=False)

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

