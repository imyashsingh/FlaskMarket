from flask import render_template,request,flash,redirect,url_for

from market import app
from market import db
from market.models import Blog,User
from market.forms import RegisterForm,LoginForm, BlogForm
from flask_login import login_user, current_user, logout_user, login_required


# home page route 
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

# Register and Login routes
@app.route('/register',methods=['GET','POST'])
@app.route('/register_page',methods=['GET','POST'])
def register_page():
    form=RegisterForm()

    # If the form is submitted, validate it and process the data
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email_address=form.email_address.data,
        )
        new_user.set_password(form.password1.data)
        db.session.add(new_user)
        db.session.commit()
        print(f'User {new_user.username} has been created successfully!')
        # Redirect to the market page or any other page after successful registration
        flash('Account created!', category='success')
        login_user(new_user)
        return redirect(url_for('market_page'))
    if form.errors:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


# Login route
@app.route('/login',methods=['GET','POST'])
@app.route('/login_page',methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash(f'Welcome back, {user.username}!', category='success')
            login_user(user)
            # Redirect to the market page or any other page after successful login
            return redirect(url_for('market_page'))
        else:
            flash('Login Unsuccessful. Please check username and password', category='danger')

    return render_template('login.html',form=form)

# Logout route
@app.route('/logout')
@app.route('/logout_page')
@login_required
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('home_page'))



@app.route('/market')
@app.route('/market_page')
def market_page():
    query = request.args.get('q')
    if query:
        blogs = Blog.query.filter(
            Blog.title.ilike(f"%{query}%") | Blog.content.ilike(f"%{query}%") | Blog.owner.ilike(f"%{query}%")
        ).order_by(Blog.created_at.desc()).all()
    else:
        blogs = Blog.query.order_by(Blog.created_at.desc()).all()
        
    return render_template('market.html', blogs=blogs)

@app.route('/blog/<int:blog_id>')
def blog_detail(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if not blog:
        flash('Blog not found.', category='danger')
        return redirect(url_for('market_page'))
    # Render the blog detail page with the blog data
    return render_template('blog_detail.html', blog=blog)



# Create blog route
@app.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    form=BlogForm()
    if form.validate_on_submit():
        new_blog = Blog(
            title=form.title.data,
            content=form.content.data,
            owner=current_user.id  # Associate the blog with the current user
        )
        db.session.add(new_blog)
        db.session.commit()
        flash(f'Blog "{new_blog.title}" created successfully!', category='success')
        return redirect(url_for('market_page'))
    if form.errors:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating the blog: {err_msg}', category='danger')
    return render_template('blog_form.html', form=form)

# Edit blog route
@app.route('/edit_blog/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def edit_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    # Check ownership
    if blog.owner != current_user.id:
        flash('You do not have permission to edit this blog.', category='danger')
        return redirect(url_for('market_page'))

    # Pre-fill form with blog data
    form = BlogForm(obj=blog)
    if form.validate_on_submit(): 
        form.populate_obj(blog)
        db.session.commit()
        flash(f'Blog "{blog.title}" updated successfully!', category='info')
        return redirect(url_for('market_page'))

    return render_template('blog_form.html', form=form, blog=blog)

# Delete blog route
@app.route('/delete_blog/<int:blog_id>', methods=['POST'])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    # Check ownership
    if blog.owner != current_user.id:
        flash('You do not have permission to delete this blog.', category='danger')
        return redirect(url_for('market_page'))
    db.session.delete(blog)
    db.session.commit()
    flash(f'Blog "{blog.title}" deleted successfully!', category='danger')
    return redirect(url_for('market_page'))
