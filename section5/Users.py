import sqlite3
from flask_restful import Resource, reqparse


class User:

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        filter_query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(filter_query, (username, ))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        filter_query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(filter_query, (_id, ))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                type=str,
                required=True,
                help = 'fill that part'
    )
    parser.add_argument('password',
                type=str,
                required=True,
                help='fill that part'
    )

    def post(self):

        data = self.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "username already taken"}

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()


        create_user_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(create_user_query, (data['username'], data['password']))


        connection.commit()
        connection.close()

        return {"message": "user created successfully!"}, 201
