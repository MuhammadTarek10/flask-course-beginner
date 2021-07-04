from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help='fill that part'
    )

    parser.add_argument('store_id',
            type=int,
            required=True,
            help='fill that part'
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"message": "item not found!"}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "item {} already exists".format(name)}, 400

        data = self.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_database()
        except:
            return {"message": "an error occurred in inserting"}, 500

        return item.json(), 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            delete_from_database(item)
            return {"message": "item named {} is deleted".format(name)}
        return {"message": "no item named {}!".format(name)}


    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']


        item.save_to_database()
        return item.json()


class ItemList(Resource):

    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
