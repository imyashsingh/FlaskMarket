from flask import render_template

from market import app
from market.models import Item


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