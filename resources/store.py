from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        else:
            return {"message": "no store named {}".format(name)}, 404


    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "store already exists"}

        store = StoreModel(name)

        try:
            store.save_to_database()
        except:
            return {"message": "error in inserting"}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_database()
            return {"message": "store deleted"}
        else:
            return {"message": "no store named {}".format(name)}, 404

class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
