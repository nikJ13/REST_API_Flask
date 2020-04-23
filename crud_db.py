from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname('crud_db.py'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.db')
app.config['SECRET_KEY'] = "\x04w\x94\xc5\xb0dT\xe4nY1\x97\x87Sz\x1b!\x07\xfb'\xb5\xfc\xe5m"
app.config['DEBUG'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/user", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']
    
    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dumps(new_user))
	

# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    return jsonify(users_schema.dumps(all_users))

# endpoint to get user detail by id
@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)
	
# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email  
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)

# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)
   
if __name__ == '__main__':
    app.run(debug=True)
	

