from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister,User,UserLogin,TokenRefresh,UserLogout
from resources.item import Item,ItemList
from resources.store import Store,StoreList
from db import db
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFIACTIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
api = Api(app)
app.secret_key = "jose"
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

jwt = JWTManager(app)    # /auth

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items/')
api.add_resource(UserRegister,'/register')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserLogin,'/login')
api.add_resource(TokenRefresh,'/refresh')
api.add_resource(UserLogout,'/logout')

if __name__ == "__main__":
    app.run(port=5000,debug=True)