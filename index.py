from flask import Flask
from dotenv import load_dotenv
from connectors.mariadb_connector import connection

from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, select
from models.product import Product

load_dotenv()


app = Flask(__name__)

@app.route("/")
def hello_world():

    # Session = sessionmaker(connection)
    # with Session() as s:
    #     s.execute(text("INSERT INTO product(name, price, description) VALUES ('tas', 90000, 'ini tas mahal')"))
    #     s.commit()

        
    # insert data using SQLalchemy
    # newProduct = Product(name = "pisau lipat", price = 100000, description= "made with loft")
    # session = sessionmaker(connection)
    # with session() as s:
    #     s.add(newProduct)
    #     s.commit()

    # Fetch all products from database using ORM
    product_query = select(Product)
    session = sessionmaker(connection)
    with session() as s:
        result = s.execute(product_query)
        for row in result.scalars():
            print(f'id: {row.id}, name: {row.name}, price: {row.price}')


    return "hello world"