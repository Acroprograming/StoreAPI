from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store=StoreModel.find_by_name(name)
        if(store):
            return store.json()
        return {"message":"Store not found"},404
    
    def post(self,name):
        store=StoreModel.find_by_name(name)
        if(store):
            return {"message":"Store already exists"},400
        store=StoreModel(name)
        store.save_to_db()
        return {"message":"Store Created Successfully"},201
    
    def delete(self,name):
        store=StoreModel.find_by_name(name)
        if(store):
            store.delete_from_db()
            return {"message":"Store Deleted Successfully"}
        return {"message":"Store not found"},404
        

class Stores(Resource):
    def get(self):
        return {"stores":[store.json() for store in StoreModel.query.all()]}
    