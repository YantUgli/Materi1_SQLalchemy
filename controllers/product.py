from flask import Blueprint, request
from connectors.mariadb_connector import connection
from models.product import Product

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity

product_blueprint = Blueprint("product_bluepring", __name__)


@product_blueprint.route("/product", methods=['GET'])
# @login_required
@jwt_required()
def get_products():

    session = sessionmaker(connection)
    s = session()
    
    try:
        product_query = select(Product)

        search_keyword = request.args.get('query')
        if search_keyword != None:
            product_query = product_query.where(Product.name.like(f"%{search_keyword}%"))

        result = s.execute(product_query)

        products = []

        # products = products.scalars()
        for row in result.scalars():
            products.append({
                'id' : row.id,
                'name' : row.name,
                'price' : row.price,
                'description' : row.description
            })

    except Exception as e:
        print(e)

        return {'message' : "unexpected Error"}, 500
    

    return {'message' : 'success fetch product data',
            'products' : products,
            'user' : current_user.name
            }


@product_blueprint.route("/product", methods=['POST'])
def insert_product():

    session = sessionmaker(connection)
    s = session()
    s.begin()

    try:
        new_product = Product(
            name = request.form['name'],
            price = request.form['price'],
            description = request.form['description']

        )
        print(new_product)
        s.add(new_product)
        s.commit()


    except Exception as e:   
        s.rollback()
        return {"message": "faill to insert"}, 500


    return {'message' : 'success insert product data'}, 200

@product_blueprint.route("/product/<id>", methods=['DELETE'])
def delete_product(id):
    session = sessionmaker(connection)
    s = session()
    s.begin()

    try:
        product = s.query(Product).filter(Product.id == id).first()
        s.delete(product)
        s.commit()
    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "fail to delted data"}, 500
    
    return {'message' : 'success Delete product data'},200

@product_blueprint.route("/product/<id>", methods=['PUT'])
def update_product(id):
    session = sessionmaker(connection)
    s = session()
    s.begin()
    
    try:
        product = s.query(Product).filter(Product.id == id).first()
        product.name = request.form['name']
        product.price = request.form['price']
        product.description = request.form['description']

        s.commit()
    except Exception as e:
        s.rollback()
        return {"message": "fail to update data"}, 500

    
    return {'message' : 'success Update product data'}, 200

