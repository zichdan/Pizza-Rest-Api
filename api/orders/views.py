from flask_restx import Namespace, Resource, fields
from ..models.orders import Order
from..models.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import db



order_namespace = Namespace("orders", description= "A namespace for Orders")


order_model = order_namespace.model(
    'Order', {
        'id': fields.Integer(description="input for an ID"),
        'size': fields.String(description="input for side",required=True,
                              enum=['SMALL','MEDIUM', 'LARGE', 'EXTRA_LARGE']),        
        'order_status': fields.String(description="input for order status", required=True,
                                      enum=['PENDING', 'IN_TRANSATION', 'DELIVERED'])
    }
)
    
    
order_status_model = order_namespace.model(
    'Order_Status', {
        "order_status": fields.String(required=True, description="input for order_status update", 
            enum = ["PENDING", "IN_TRANSATION", "DELIVERED"] 
        )
    }
)

@order_namespace.route("/orders")
class OrderGetCreate(Resource):
    
    @order_namespace.marshal_with(order_model)
    def get(self):
        '''
        Get all order 
        '''
        orders = Order.query.all() 
        
        return orders ,HTTPStatus.OK
    
    
    @jwt_required()
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    def post (self):
        '''
        place a new order
        '''
        
        username= get_jwt_identity()
        
        current_user=User.query.filter_by(username=username).first()
        
        data = order_namespace.payload

        new_order = Order(
            size=data['size'],
            quantity=data['quantity'],
            flavour=data['flavour']
        )
        
        new_order.User=current_user
        
        new_order.save()
        
        return new_order, HTTPStatus.CREATED 
        
    
    
    
@order_namespace.route("/order/<int:order_id>")
class GetUpdateDelete(Resource):
    
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self, order_id):
        '''
        Retrieving order by id
        '''
        order = Order.get_by_id(order_id)
        
        return order, HTTPStatus.OK    
    
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def put(self, order_id):
        '''
        Updating Order by id
        '''
        
        order_to_update = Order.get_by_id(order_id)
        
        data = order_namespace.payload 
        
        order_to_update.quantity = data['quantity']
        order_to_update.size = data['size']
        order_to_update.flavour = data['flavour']
        
        db.session.commit()
        
        return order_to_update, HTTPStatus.OK
        
        
    @jwt_required()
    @order_namespace.marshal_with(order_model)
    def post(self, order_id):
        '''
        Deleting Oder by id
        '''
        order_to_delete = Order.get_by_id(order_id)
        
        order_to_delete.delete()
        
        return order_to_delete, HTTPStatus.NO_CONTENT
        
     
    
@order_namespace.route("/user/<int:user_id>/order/<int:order_id>")

class GetSpecificOderByUser(Resource):
    
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    # @jwt_required()
    def get(self, user_id, order_id):
        '''
        Get a User's Specific Order
        '''
        user = User.get_by_id(user_id)    
        
        order = Order.query.filter_by(id=order_id).filter_by(User=user).first()
        
        return order, HTTPStatus.OK    
    
    
    
@order_namespace.route("/user/<int:user_id>/orders")
class UserOrders(Resource):
    
    @order_namespace.marshal_list_with(order_model)
    @jwt_required()
    def get(self, user_id):
        '''
        Get all orders one particular user has made
        '''
        user = User.get_by_id(user_id)
        
        orders = user.orders
        
        return orders, HTTPStatus.OK
    
    
    
    
    @order_namespace.route("/order/status/<int:order_id>")
    class UpdateOrderStatus(Resource):
    
        
        @order_namespace.expect(order_status_model)
        @order_namespace.marshal_with(order_model)
        @jwt_required()
        def patch(self, order_id):
            '''
            Update an order's Status
            '''
            data = order_namespace.payload
            
            order_to_update = Order.get_by_id(order_id)
            
            order_to_update.order_status = data["order_status"]
            
            db.session.commit()
            
            return order_to_update, HTTPStatus.OK
        
        
        
        