from flask import render_template, redirect, url_for,abort,request
from . import main
from flask_login import login_required,current_user
from ..models import User,Pitch,Comment,Upvote,Downvote
from .forms import UpdateProfile,PitchForm,CommentForm
from .. import db,photos


# this will add index file route

@main.route('/')
def index():
    pitches = Pitch.query.all()
    interview = Pitch.query.filter_by(category = 'Interview').all()
    product = Pitch.query.filter_by(category = 'Product').all()
    promotion = Pitch.query.filter_by(category = 'Promotion').all()

    return render_template('index.html',pitches=pitches, interview=interview,product=product,promotion=promotion)

# this will add new pitch page route

@main.route('/create_new', methods = ['POST','GET'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user
        new_pitch_object = Pitch(post=post,user_id=current_user._get_current_object().id,category=category,title=title)
        new_pitch_object.save_p()
        return redirect(url_for('main.index'))
        
    return render_template('new_pitch.html', form = form)

# this is the add comments route

@main.route('/comment/<int:pitch_id>', methods = ['POST','GET'])
@login_required
def comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,pitch_id = pitch_id)
        new_comment.save_c()
        return redirect(url_for('.comment', pitch_id = pitch_id))
    return render_template('comment.html', form =form, pitch = pitch,all_comments=all_comments)


# this will add user profile information

@main.route('/user/<name>')
def profile(name):
    user=User.query.filter_by(username=name).first()
    user_id=current_user._get_current_object().id
    posts=Pitch.query.filter_by(user_id=user_id).all()
    if user is None:
        abort(404)
        
    return render_template("profile/prfile.html", user=user, posts=posts)    
