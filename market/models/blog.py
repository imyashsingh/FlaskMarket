from sqlalchemy.sql import func
from market import db


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Blog {self.name}>'
