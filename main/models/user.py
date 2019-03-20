from database.db import db
from main.authenticate.security import bcrypt


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500))
    password = db.Column(db.String(500))
    items = db.relationship('ItemModel',
                            lazy='dynamic',
                            cascade='all, delete-orphan')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @staticmethod
    def generate_hash(password):
        return bcrypt.generate_password_hash(password)

    @staticmethod
    def verify_hash(hash, password):
        return bcrypt.check_password_hash(hash, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
