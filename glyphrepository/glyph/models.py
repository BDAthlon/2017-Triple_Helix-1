# -*- coding: utf-8 -*-
"""Glyph models."""
from __future__ import division

from glyphrepository.database import Column, Model, SurrogatePK, db, reference_col, relationship

from flask import current_app as app
import os

class Glyph(SurrogatePK, Model):
    """A glyph."""

    __tablename__ = 'glyphs'
    name = Column(db.String(80), unique=False, nullable=False)
    file_name = Column(db.String(80), unique=False, nullable=False)

    has_pdf = Column(db.Boolean)
    has_png = Column(db.Boolean)
    has_svg = Column(db.Boolean)
    has_jpg = Column(db.Boolean)

    has_specification_pdf = Column(db.Boolean)
    has_specification_png = Column(db.Boolean)
    has_specification_svg = Column(db.Boolean)
    has_specification_jpg = Column(db.Boolean)

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
        # avoid multiply counting ratings from the same user
        users = []
        ratings = []
        for comment in self.comments:
            if comment.rating >= 0 and comment.user_id not in users:
                ratings.append(comment.rating)
                users.append(comment.user_id)

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

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in set(['pdf', 'png', 'jpg', 'jpeg', 'svg'])

    def save_glyph_file(self, f):
        file_name = f.filename

        if Glyph.allowed_file(file_name):
            UPLOAD_FOLDER = os.path.join(app.root_path, 'static/glyphs')
            file_extension = os.path.splitext(file_name)[-1].lower().replace('jpeg', 'jpg')
            filename = str(self.id) + file_extension

            f.save(os.path.join(UPLOAD_FOLDER, filename))
            self.record_file(file_extension)
            return True

    def save_specification_file(self, f):
        file_name = f.filename

        if Glyph.allowed_file(file_name):
            UPLOAD_FOLDER = os.path.join(app.root_path, 'static/glyphs')
            file_extension = os.path.splitext(file_name)[-1].lower().replace('jpeg', 'jpg')
            filename = str(self.id) + "_specification" + file_extension

            f.save(os.path.join(UPLOAD_FOLDER, filename))
            self.record_spec_file(file_extension)

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

    def record_spec_file(self, file_extension):
        if file_extension[0] == ".":
            file_extension = file_extension[1:]

        if file_extension == "pdf":
            self.has_specification_pdf = True
        elif file_extension == "png":
            self.has_specification_png = True
        elif file_extension == "svg":
            self.has_specification_svg = True
        elif file_extension == "jpg":
            self.has_specification_jpg = True

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

    def get_preferred_specification_filename(self):
        if self.has_specification_png:
            return str(self.id) + "_specification.png"
        elif self.has_specification_svg:
            return str(self.id) + "_specification.svg"
        elif self.has_specification_jpg:
            return str(self.id) + "_specification.jpg"
        elif self.has_specification_pdf:
            return str(self.id) + "_specification.pdf"
        else:
            return ""