from flask import Flask,render_template

app=Flask(__name__)


items = [
        {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
        {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
        {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    ]

# home page route 
@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')

# market page route
@app.route('/market')
def market():
    context={ 'items': items}
    return render_template('market.html',**context)

if __name__ == '__main__':
    app.run(debug=True)