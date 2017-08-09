# -*- coding: utf-8 -*-
"""BO term models."""

from glyphrepository.database import Column, Model, SurrogatePK, db, reference_col, relationship

class SOterm(SurrogatePK, Model):
    """A glyph."""

    __tablename__ = 'soterms'
    name = Column(db.String(80), unique=False, nullable=False)
    definition = Column(db.String(500), unique=False, nullable=False)

    is_a = reference_col('soterms', nullable=True)
    parent = relationship('SOterm')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)

    def get_full_id(self):
        return "SO:" + str(self.id).zfill(7)