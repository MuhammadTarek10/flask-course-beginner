import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required



class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help='fill that part'
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item

        return {"message": "item not found!"}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        get_item_query = "SELECT * FROM items WHERE name=?"
        item = cursor.execute(get_item_query, (name, )).fetchone()
        connection.close()

        if item:
            return {"item": {"name": item[0], "price": item[1]}}
        return None


    def post(self, name):
        if self.find_by_name(name):
            return {"message": "item {} already exists".format(name)}, 400

        data = self.parser.parse_args()
        item = {"name": name, "price": data['price']}
        try:
            self.insert_item(item)
        except:
            return {"message": "an error occurred in inserting"}, 500

        return item, 201

    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        add_item_query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(add_item_query, (item['name'], item['price']))

        connection.commit()
        connection.close()


    def delete(self, name):
        item = self.find_by_name(name)
        if not item:
            return {"message": "item not found!"}, 404

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        delete_item_query = "DELETE FROM items WHERE name=?"
        cursor.execute(delete_item_query, (name, ))


        connection.commit()
        connection.close()

        return {"message": "item deleted successfully!"}, 200


    def put(self, name):
        item = self.find_by_name(name)
        data = self.parser.parse_args()
        updated_item = {"name": name, "price": data['price']}


        if not item:
            try:
                self.insert_item(updated_item)
            except:
                return {"message": "an error occurred in inserting"}, 500
        else:
            try:
                self.update_item(updated_item)
            except:
                return {"message": "an error occurred in updating"}, 500

        return updated_item


    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        delete_item_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(delete_item_query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):

    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        items = []

        get_all_items_query = "SELECT * FROM items"
        for row in cursor.execute(get_all_items_query):
            items.append({'name': row[0], 'price': row[1]})


        connection.close()
        return {"items": items}
