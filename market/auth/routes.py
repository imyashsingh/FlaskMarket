from flask import render_template,request,flash,redirect,url_for

from . import auth_bp
from market import db
from market.models import Blog,User
from .forms import RegisterForm,LoginForm
from flask_login import login_user, logout_user, login_required


# home page route 
@auth_bp.route('/')
@auth_bp.route('/home')
def home_page():
    return render_template('auth/home.html')

# Register and Login routes
@auth_bp.route('/register',methods=['GET','POST'])
@auth_bp.route('/register_page',methods=['GET','POST'])
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
        return redirect(url_for('blog.market_page'))
    if form.errors:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('auth/register.html', form=form)


# Login route
@auth_bp.route('/login',methods=['GET','POST'])
@auth_bp.route('/login_page',methods=['GET','POST'])
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
            return redirect(url_for('blog.market_page'))
        else:
            flash('Login Unsuccessful. Please check username and password', category='danger')

    return render_template('auth/login.html',form=form)

# Logout route
@auth_bp.route('/logout')
@auth_bp.route('/logout_page')
@login_required
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('auth.home_page'))

