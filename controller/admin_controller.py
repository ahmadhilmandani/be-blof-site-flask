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
