from flask import json
from flask_restx import Resource, reqparse
from flask_restx import Namespace
from app.utils.updating_products import updating_list_products
from ...utils.redis_client import find_or_add, get_redis
from ...models.product import ProductModel
from flask_jwt_extended import jwt_required
from ...utils.paginate import paginate_query

product_ns = Namespace("products", description="Product-related operations")

@product_ns.route("/")
class Products(Resource):
    @jwt_required()
    def get(self):
        redis_client = get_redis()
        cache_key = "products:list"

        cached = redis_client.get(cache_key)
        if cached:
            return paginate_query(json.loads(cached))

        products_data = find_or_add(redis_client, cache_key, [product.json() for product in ProductModel.query.all()])
        return paginate_query(products_data)
    
    @jwt_required()
    def post(self):
        data = Product.argument.parse_args()

        product = ProductModel(**data)

        try:
            product.save_product()
        except Exception as e:
            return { 'message': str(e) }, 500

        updating_list_products()

        return product.json(), 201

@product_ns.route("/<uuid:id>/")
class Product(Resource):
    argument = reqparse.RequestParser()
    argument.add_argument('name', type=str, required=True, help="The field 'name' cannot be left blank")
    argument.add_argument('mark', type=str, required=True, help="The field 'mark' cannot be left blank")
    argument.add_argument('value', type=float, required=True, help="The field 'value' cannot be left blank")
    
    @jwt_required()
    def get(self, id):
        product = ProductModel.find_product(id)
        if product: 
            return product.json()    
        return { 'message': 'Product not found.' }, 404

    @jwt_required()
    def put(self, id):
        data = Product.argument.parse_args()

        product_found = ProductModel.find_product(id)
        
        if product_found:
            product_found.update_product(**data)
            try:
                product_found.save_product()
            except:
                return { 'message': 'An interval error ocurred trying to save product.' }, 500
            
            updating_list_products()

            return product_found.json(), 200
        
    @jwt_required()
    def delete(self, id):
        product = ProductModel.find_product(id)
        if product:
            try:
                product.delete_product()
                updating_list_products()
                return { 'message': 'Product deleted successfully.' }, 200
            except Exception as e:
                print(f"Error deleting product: {str(e)}")
                print(f"Error type: {type(e)}")
                import traceback
                traceback.print_exc()
                
                return { 'message': f'An internal error occurred: {str(e)}' }, 500
        else:
            return { 'message': 'Product not found.' }, 404
