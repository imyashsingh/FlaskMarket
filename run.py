from market import app
from market.models import db, Item ,User

if __name__ == '__main__':
    app.run(debug=True)