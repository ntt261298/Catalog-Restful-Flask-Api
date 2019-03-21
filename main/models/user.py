from database.db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    items = db.relationship('ItemModel',
                            lazy='dynamic',
                            cascade='all, delete-orphan')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
