from flask_restful import Resource, reqparse
from flask_jwt_extended import ( 
jwt_required,
get_jwt,
get_jwt_identity
)
from models.item import ItemModel


class Item(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('price', type=float,required=True,help='Price value is required')
    parser.add_argument('store_id', type=int,required=True,help='Item must be linked to a store_id')
    
    @jwt_required()
    def get(self,name):
        item=ItemModel.find_by_name(name)
        if(item):
            return item.json(),200
        return {'message':"Item not found"},404
        
    
    def post(self,name):
        if(ItemModel.find_by_name(name)):
            return {'message':"Item already exists"},400
        data=Item.parser.parse_args()
        new_item=ItemModel(name,**data)
        try:
            new_item.save_to_db()
        except:
            return {'message':'An error occurred while inserting the item'},500
        return new_item.json(),201
    
    @jwt_required(fresh=True)
    def delete(self,name):
        claims=get_jwt()
        if not claims["is_admin"]:
            return {"message": "You are not allowed to delete"},401
        item=ItemModel.find_by_name(name)
        if item is None:
            return {"message":'item not found'},404
        item.delete_from_db()
        return {"message":'item deleted successfully'}
    
    @jwt_required()
    def put(self,name):
        data=Item.parser.parse_args()
        item=ItemModel.find_by_name(name)
        if(item):
            item.price=data['price']
        else:
            item=ItemModel(name,**data)
        item.save_to_db()
        return {'message':'data updated successfully'}  
            

class Items(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id=get_jwt_identity()
        if(user_id==None):
            return {"items":[item.name for item in ItemModel.query.all()]}
        return {"items":[item.json() for item in ItemModel.query.all()]}
