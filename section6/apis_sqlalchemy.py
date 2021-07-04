from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authentication, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db/'
app.config['SQLALCEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Tarek'
api = Api(app)

jwt = JWT(app, authentication, identity)


@app.before_first_request
def create_table():
    db.create_all()

api.add_resource(Item, "/item/<string:name>")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")


if __name__ == "__main__":
    from real_sql_alchemy import db
    db.init_app(app)
    app.run(port=5000, debug=True)
