from flask import Blueprint, redirect, render_template, url_for, request, flash
from flask_login import login_required, current_user

from glyphrepository.utils import flash_errors

from glyphrepository.comment.models import Comment
from glyphrepository.comment.forms import CommentForm

blueprint = Blueprint('comment', __name__, static_folder='../static', url_prefix='/comment',)


@blueprint.route('/<comment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    """Edit a comment"""
    comment = Comment.query.filter(Comment.id == comment_id).first()

    if comment.user != current_user:
        flash('Not your comment!', 'warning')
        return redirect(url_for('glyph.view'), glyph=comment.glyph)

    form = CommentForm(request.form, name=comment.name, rating=comment.rating, comment=comment.comment)

    if form.validate_on_submit() and request.method == 'POST':
        comment.update(name=form.name.data, rating=form.rating.data, comment=form.comment.data, user_id=current_user.id,
                       glyph_id=comment.glyph_id)
        comment.save()

        # ensure all comments from same user give same rating
        for c in Comment.query.filter(Comment.user_id==current_user.id, Comment.glyph_id==comment.glyph_id).all():
            c.rating = form.rating.data
            c.save()

        flash('Comment successfully added.', 'success')
        return redirect(url_for('glyph.show_glyph', glyph_id=comment.glyph_id))
    else:
        flash_errors(form)

    return render_template('comment/add-comment.html', form=form)


