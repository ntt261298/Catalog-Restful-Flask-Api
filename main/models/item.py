from database.db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    description = db.Column(db.String(5000))
    cat_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    # category = db.relationship('CategoryModel')

    def __init__(self, title, description, cat_id, user_id):
        self.title = title
        self.description = description
        self.cat_id = cat_id
        self.user_id = user_id

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
