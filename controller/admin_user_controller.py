from app import db
from models.users import User
from flask import jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()

# logic: register
def register_user():
  data = request.get_json()
    
  name = data.get('name')
  email = data.get('email')
  short_bio = data.get('short_bio')
  password = data.get('password')
  hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
  role = 'user'

  new_writer = User(name=name, email=email, short_bio=short_bio, role=role, password=hashed_password)
  db.session.add(new_writer)
  db.session.commit()
  
  return jsonify({
      'message': 'user created', 
      'data': {'name': name, 'email': email, 'short_bio': short_bio, 'role': role}
      }), 201

# logic: add writer
def add_writer(id):
  get_user = User.query.get_or_404(id)
  
  get_user.role = 'writer'

  db.session.commit()

  return jsonify({
      'message': 'Writer Added',
      }), 200


# logic: login
def login():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')

  get_user = User.query.filter_by(email=email).first()
  
  if get_user and bcrypt.check_password_hash(get_user.password, password):
     token = create_access_token(identity={'id': get_user.id, 'name': get_user.name, 'email': get_user.email, 'is_verif': get_user.is_verif, 'role': get_user.role})
     return jsonify({
            'data': { 'name': get_user.name, 'email': get_user.email, 'short_bio': get_user.short_bio, 'role': get_user.role, 'is_verif': get_user.is_verif, 'token': token }
      }), 200
    
  return jsonify({'error': True, 'message': "Invalid Email or password"}), 401


# logic: update profile
def profile_update(id):
  get_user = User.query.get_or_404(id)
    
  data = request.get_json()
  get_user.name = data.get('name')
  get_user.email = data.get('email')
  get_user.short_bio = data.get('short_bio')
  get_user.password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')

  db.session.commit()

  token = create_access_token(identity=get_user)

  return jsonify({
        'data': { 'name': get_user.name, 'email': get_user.email, 'short_bio': get_user.short_bio, 'role': get_user.role, 'is_verif': get_user.is_verif, 'token': token }
  }), 200
