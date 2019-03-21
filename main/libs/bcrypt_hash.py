from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def generate_hash(password):
    return bcrypt.generate_password_hash(password)


def verify_hash(hash, password):
    return bcrypt.check_password_hash(hash, password)
