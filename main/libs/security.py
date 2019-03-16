from main.models.user import UserModel
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    user = UserModel.find_user_by_username(username)
    if user is None:
        return None
    if safe_str_cmp(user.password, password):
        return user
    return None


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_user_by_id(user_id)
