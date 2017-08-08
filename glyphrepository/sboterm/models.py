# -*- coding: utf-8 -*-
"""SBO term models."""

from glyphrepository.database import Column, Model, SurrogatePK, db, reference_col, relationship

class SBOterm(SurrogatePK, Model):
    """A glyph."""

    __tablename__ = 'sboterms'
    name = Column(db.String(80), unique=False, nullable=False)
    definition = Column(db.String(500), unique=False, nullable=False)

    is_a = reference_col('sboterms', nullable=True)
    parent = relationship('SBOterm')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)

