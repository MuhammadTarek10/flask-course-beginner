from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authentication, identity

app = Flask(__name__)
app.secret_key = 'Tarek'
api = Api(app)

jwt = JWT(app, authentication, identity)


items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help='fill that part'
    )

    @jwt_required()
    def get(slef, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name']==name, items), None) is not None:
            return {"message": "item named '{}' already exists".format(name)}, 400
        data = self.parser.parse_args()
        item = {"name": name, "price": data['price']}
        items.append(item)
        return item, 201 # 201 for creation

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {"message": "deleted"}


    def put(self, name):
        data = self.parser.parse_args()
        try:
            item = next(filter(lambda x: x['name'] == name, items))
        except:
            item = None
        if item is None:
            item = {"item": name, "price": data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")


app.run(port=5000, debug=True)
