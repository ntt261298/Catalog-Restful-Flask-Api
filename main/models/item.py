from datetime import datetime

from main.libs.database import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(),
                           nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, description, category_id, user_id):
        self.title = title
        self.description = description
        self.category_id = category_id
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)

    def delete_from_db(self):
        db.session.delete(self)
