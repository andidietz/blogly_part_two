from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'secret-goes-here'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def users_page_redirect():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('/list.html', users=users)

@app.route('/users/new')
def show_new_user_form():
    return render_template('/new_user.html')

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('/user_details.html', user=user)

@app.route('/users/new', methods=['POST'])
def submit_new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('/user_edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def submit_edited_user(user_id):
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')

# posts

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('/post_details.html', post=post)

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('/new_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def submit_new_post(user_id):
    user = User.query.get_or_404(user_id)
    
    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user=user)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('/post_edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_edited_post(post_id):
    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')