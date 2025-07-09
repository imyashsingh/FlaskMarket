from flask import render_template,request,flash,redirect,url_for

from market import app
from market import db
from market.models import Item,User
from market.forms import RegisterForm


# home page route 
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

# market page route
@app.route('/market')
def market():
    items=Item.query.all()
    context={ 'items': items}
    return render_template('market.html',**context)

@app.route('/register',methods=['GET','POST'])
@app.route('/register_page',methods=['GET','POST'])
def register_page():
    form=RegisterForm()

    # If the form is submitted, validate it and process the data
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                username=form.username.data,
                email_address=form.email_address.data,
                password_hash=form.password1.data 
            )
            db.session.add(new_user)
            db.session.commit()
            print(f'User {new_user.username} has been created successfully!')
            # Redirect to the market page or any other page after successful registration
            return redirect(url_for('market'))
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}')
    context = {'form': form}
    return render_template('register.html', **context)