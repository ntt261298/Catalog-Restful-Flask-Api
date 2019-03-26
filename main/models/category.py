from main.libs.database import db


class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)

    items = db.relationship('Items', cascade='all, delete-orphan')

    def __init__(self, name):
        self.name = name
