from app import db
from models.users import User
from flask import jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

# logic for verif writer
def verif_writer(id):
  get_user = User.query.get_or_404(id)
    
  get_user.is_verif = True

  db.session.commit()

  return jsonify({
        'message': 'user verification'
  }), 200


# logic: get user
def get_all_user():
  users = User.query.filter(User.role!='admin').all()
  return jsonify({
                  'data': [{ 
                  'id': user.id,
                  'name': user.name, 
                  'role': user.role, 
                  'is_verif': user.is_verif, 
                  } for user in users]
                }), 200


# logic: get user need a verification
def get_writer_need_verif():
   users = User.query.filter(User.role=='writer',User.is_verif==0).all()
   return jsonify({
                  'data': [{ 
                  'id': user.id,
                  'name': user.name, 
                  'role': user.role, 
                  'is_verif': user.is_verif, 
                  } for user in users]
                }), 200