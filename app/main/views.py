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


