from market import db
from market import bycrypt
from market import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    def set_password(self,password):
        self.password_hash = bycrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self,password):
        return bycrypt.check_password_hash(self.password_hash, password)


class Item(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(100),nullable=False,unique=True)
    barcode= db.Column(db.String(100),nullable=False,unique=True)
    price= db.Column(db.Float,nullable=False)
    description= db.Column(db.String(200),nullable=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'Item {self.name}'
    

