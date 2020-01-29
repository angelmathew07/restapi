from flask_restful import reqparse,Resource
from flask_jwt import jwt_required
import sqlite3
from models.store import StoreModel

class Store(Resource):

    parser=reqparse.RequestParser()
    parser.add_argument("price",
    type=float,
    required=True,
    help="this field is required"
    )
    parser.add_argument("store_id",
    type=int,
    required=True,
    help="tstore id is required"
    )

    @jwt_required()
    def get(self,name):
        item=StoreModel.find_by_name(name)
        if item:
            return item.json()
        return {"message":"Item not found"},404


    def post(self,name):
        if(StoreModel.find_by_name(name)):
            return{"message":"A Store with name {} already exists".format(name)},400
        store=StoreModel(name)
        # item=ItemModel(name,data['price'],data['store_id'])
        try:
            store.save_to_db()
        except:
            return {"message":"Error occured while inserting item"},500
        
        return store.json(), 201

  
    def delete(self,name):
        store=StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message':"Store deleted"}
        

class StoreList(Resource):
    def get(self):
        return {"stores":[store.json() for store in StoreModel.query.all()]}