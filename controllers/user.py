from flask import Blueprint, request
from connectors.mariadb_connector import connection
from models.user import User

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import create_access_token

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/register',methods=['POST'])
def register_user():
    session = sessionmaker(connection)
    s = session()
    s.begin()

    try:
        newUser= User(
            name =request.form['name'],
            email = request.form['email'],
        )
        newUser.set_password(request.form['password'])

        s.add(newUser)
        s.commit()
    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "fail to register"}, 400
    

    return {"message" : "Register success"}

@user_blueprint.route('/login', methods=['POST'])
def login_handle():
    session = sessionmaker(connection)
    s = session()

    s.begin()

    try:
        email = request.form['email']
        user = s.query(User).filter(User.email == email).first()

        if user == None:
            return{"message" : "User not found"}, 403
        
        if not user.check_password(request.form['password'] ):
            return {"message": "invalid password"}, 403
        
        # Bisa login
        login_user(user)

        # get session id
        session_id = request.cookies.get('session')

        return {
            "session_id" : session_id,
            "message": "login success"
        }, 200

    except Exception as e:
        print(e)
        s.rollback()
        return {"message" : "gagal login"}
    

@user_blueprint.route('/logout', methods=['GET'])
@login_required
def user_logout():
    logout_user()
    return {"message": "success logout"}


@user_blueprint.route('/loginjwt', methods=['POST'])
def login_jwt():
    session = sessionmaker(connection)
    s = session()
    
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = s.query(User).filter(User.email == email).first()

        if user is None or not user.check_password(password):
            return {"message": "Invalid email or password"}, 401
        
        # membuat token JWT
        access_token = create_access_token(identity=str(user.id))

        return {
            "message": "Login JWT success",
            "access_token": access_token
        }, 200

    except Exception as e:
        print(e)
        return {"message": "Internal Server Error"}, 500
    finally:
        s.close()