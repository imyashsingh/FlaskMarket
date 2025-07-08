from flask import Flask

app=Flask(__name__)

# home page route 
@app.route('/')
def index():
    return 'Hello, World!'

# about page route
@app.route('/about/<username>')
def about(username):
    return f'This is the about page. {username}'

if __name__ == '__main__':
    app.run(debug=True)