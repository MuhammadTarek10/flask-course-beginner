from users import User


users = [
            User('1', 'Omar', 'omar_password'),
            User('2', 'amira', 'amira_password')
        ]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authentication(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user
    return None


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
