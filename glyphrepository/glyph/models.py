# -*- coding: utf-8 -*-
"""Glyph models."""

from glyphrepository.database import Column, Model, SurrogatePK, db, reference_col, relationship

class Glyph(SurrogatePK, Model):
    """A glyph."""

    __tablename__ = 'glyphs'
    name = Column(db.String(80), unique=False, nullable=False)
    file_name = Column(db.String(80), unique=False, nullable=False)

    sbo_term = Column(db.String(80), unique=False, nullable=False)

    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='glyphs')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)

