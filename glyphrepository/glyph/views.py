# -*- coding: utf-8 -*-
"""Section for viewing/editing a part."""
from flask import Blueprint, redirect, render_template, url_for, request, flash
from glyphrepository.utils import flash_errors

from glyphrepository.glyph.models import Glyph
from glyphrepository.comment.models import Comment

from glyphrepository.glyph.forms import AddGlyphForm
from glyphrepository.comment.forms import CommentForm
from glyphrepository.soterm.models import SOterm
from flask_login import login_required, current_user

blueprint = Blueprint('glyph', __name__, static_folder='../static', url_prefix='/glyph',)


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """ If no part id specified, redirect home """
    return redirect(url_for('public.home'))

@blueprint.route('/<glyph_id>', methods=['GET', 'POST'])
def show_glyph(glyph_id):
    """Show details of glyph (if it exists) or redirect home."""

    glyph_list = Glyph.query.filter(Glyph.id == glyph_id).all()

    if len(glyph_list) == 0:
        return redirect(url_for('public.home'))
    else:
        return render_template('glyph/view.html', glyph=glyph_list[0])


@blueprint.route('/<glyph_id>/comment', methods=['GET', 'POST'])
@login_required
def glyph_comment(glyph_id):
    """Comment on a glyph."""

    # User can make only one comment per glyph: if they've already made one then redirect to edit page
    comment_list = Comment.query.filter(Comment.glyph_id == glyph_id, Comment.user_id == current_user.id).all()
    if len(comment_list) > 0:
        return redirect(url_for('glyph.edit_glyph_comment', glyph_id=glyph_id))

    form = CommentForm(request.form)
    if form.validate_on_submit() and request.method == 'POST':
        Comment.create(name=form.name.data, rating=form.rating.data, comment=form.comment.data, user_id=current_user.id,
                       glyph_id=glyph_id)

        flash('Comment successfully updated.', 'success')
        return redirect(url_for('glyph.show_glyph', glyph_id=glyph_id))
    else:
        flash_errors(form)

    return render_template('comment/add-comment.html', form=form)


@blueprint.route('/<glyph_id>/comment/edit', methods=['GET', 'POST'])
@login_required
def edit_glyph_comment(glyph_id):
    """Comment on a glyph."""

    # User can make edit their comment if they have already made one; if not, redirect back to glyph page
    comment_list = Comment.query.filter(Comment.glyph_id == glyph_id and Glyph.user_id == current_user.id).all()
    if len(comment_list) == 0:
        flash('You have not yet made a comment on this glyph.', 'error')
        return redirect(url_for('glyph.show_glyph', glyph_id=glyph_id))

    comment = comment_list[0]
    form = CommentForm(request.form, name=comment.name, rating=comment.rating, comment=comment.comment)

    if form.validate_on_submit() and request.method == 'POST':
        comment.update(name=form.name.data, rating=form.rating.data, comment=form.comment.data, user_id=current_user.id,
                       glyph_id=glyph_id)
        comment.save()

        flash('Comment successfully added.', 'success')
        return redirect(url_for('glyph.show_glyph', glyph_id=glyph_id))
    else:
        flash_errors(form)

    return render_template('comment/add-comment.html', form=form)



@blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_glyph():
    """Add new glyph."""

    form = AddGlyphForm(request.form)

    options = map(lambda term: (str(term.id), term.name + " (" + term.get_full_id() + ")"), SOterm.query.all())
    options.append(("", ""))
    form.soTerm.choices = options

    if form.validate_on_submit() and request.method == 'POST':

        new_glyph = Glyph.create(name=form.name.data, file_name='', soterm_id=form.soTerm.data,
                                 user_id=current_user.id, proposal_url=form.proposal_url.data,
                                 sbol_status=form.sbol_status.data)

        valid_file = False
        for i in range(1, 5):
            file_added = new_glyph.save_glyph_file(request.files["file_path" + str(i)])
            valid_file = (valid_file or file_added)

        if not valid_file:
            new_glyph.delete()
            flash('No file found.', 'warning')
            return redirect(url_for('glyph.home'))

        for i in range(1, 5):
            new_glyph.save_specification_file(request.files["file_spec_path" + str(i)])

        flash('Glyph successfully added.', 'success')
        return redirect(url_for('glyph.show_glyph', glyph_id=new_glyph.id))

    else:
        flash_errors(form)

    return render_template('glyph/add-glyph.html', form=form)


@blueprint.route('/<glyph_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_glyph(glyph_id):
    """Edit glyph."""

    glyph = Glyph.query.filter(Glyph.id == glyph_id).first()

    if current_user != glyph.user and not current_user.is_admin:
        flash('Cannot edit - not your glyph!.', 'warning')
        return redirect(url_for('glyph.show_glyph', glyph_id=glyph_id))

    form = AddGlyphForm(request.form, name=glyph.name, soTerm=glyph.soterm, sbol_status=glyph.sbol_status, proposal_url=glyph.proposal_url)

    options = map(lambda term: (str(term.id), term.name + " (" + term.get_full_id() + ")"), SOterm.query.all())
    options.append(("", ""))
    form.soTerm.choices = options

    if form.validate_on_submit() and request.method == 'POST':

        glyph.update(name=form.name.data, soterm_id=form.soTerm.data, proposal_url=form.proposal_url.data,
                     sbol_status=form.sbol_status.data)

        for i in range(1, 5):
            glyph.save_glyph_file(request.files["file_path" + str(i)])

        for i in range(1, 5):
            glyph.save_specification_file(request.files["file_spec_path" + str(i)])

        glyph.save()

        flash('Glyph successfully updated.', 'success')
        return redirect(url_for('glyph.show_glyph', glyph_id=glyph_id))

    else:
        flash_errors(form)

    return render_template('glyph/edit-glyph.html', form=form, glyph=glyph)

