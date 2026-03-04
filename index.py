from flask import Flask
from dotenv import load_dotenv
from connectors.mariadb_connector import connection

from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, select
from models.product import Product

from controllers.product import product_blueprint
from controllers.user import user_blueprint
import os

from flask_login import LoginManager
from models.user import User
from flask_jwt_extended import JWTManager

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(product_blueprint)
app.register_blueprint(user_blueprint)

jwt = JWTManager(app)

login_manager = LoginManager()
login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     session = sessionmaker(bind=connection)
#     s = session()
#     s.query(User).get(int(user_id))

@login_manager.user_loader
def load_user(user_id):
    session = sessionmaker(connection) 
    s = session()
    user = s.query(User).get(int(user_id))
    s.close() # Penting: Tutup session agar tidak boros koneksi DB
    return user # WAJIB ADA RETURN

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
    # product_query = select(Product)
    # session = sessionmaker(connection)
    # with session() as s:
    #     result = s.execute(product_query)
    #     for row in result.scalars():
    #         print(f'id: {row.id}, name: {row.name}, price: {row.price}')


    return "hello world"