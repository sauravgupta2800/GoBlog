from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from app import db
from app.models import Post, Comment
from app.posts.forms import PostForm , CommentForm
from app.posts.utils import notifiedWhenSomeoneCommented, save_picture


posts = Blueprint("posts",__name__)
import sys

@posts.route('/post/new',methods=["GET","POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post = Post(title=form.title.data, content = form.content.data, author = current_user, image_file=picture_file)
            db.session.add(post)
            db.session.commit()
        else:
            post = Post(title=form.title.data, content = form.content.data, author = current_user)
            db.session.add(post)
            db.session.commit()

        flash("Your post has been created!",'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title="New Post",form=form,legend='New Post')







# -------------------Handling the comments-------------------

@posts.route('/post/<int:post_id>',methods=["GET","POST"])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if post==None:
        return post
    page = request.args.get('page',1,type=int)
    form = CommentForm()
    comments = Comment.query.filter_by(post=post)\
        .order_by(Comment.date_posted.desc())
    
    

    print("comments", file=sys.stdout)
    print(comments, file=sys.stdout)
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        if post.author == current_user:
            flash('Your Comment is uploaded sucessfully.','success')
        else:
            notifiedWhenSomeoneCommented(post.author, current_user,comment )
            flash('Author is notified with your comment via Email.','info')
        return redirect(url_for('posts.post',post_id=post.id))
    return render_template("post.html", title=post.title, post = post, form = form, comments = comments)


# ----------------------------



@posts.route('/post/<int:post_id>/update',methods=["GET","POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post.image_file = picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!",'success')
        return redirect(url_for("posts.post",post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title="Update Post",form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete',methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id = post_id)
    if post.author!=current_user:
        abort(403)
    for c in comments:
        db.session.delete(c)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted along with Comments!','success')
    return redirect(url_for('main.home'))




