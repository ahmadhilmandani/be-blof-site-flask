from flask import jsonify
from models.users import User
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from functools import wraps

from controller.admin_controller import verif_writer
from controller.admin_user_controller import profile_update, login, add_writer
from controller.article_controller import create_article, get_all_article, get_article_by_id, update_article, add_viewed_of_article, delete_article, most_read_article


def register_app(app):
  # create jwt insance
  jwt = JWTManager(app)

  # function to guard the endpoint that only for user role "admin"
  def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = get_jwt_identity()
        if user.role != 'admin':
            return jsonify(msg="Unauth"), 401
        return fn(*args, **kwargs)
    return wrapper
  
  
  # endpoint: add writer
  @app.route('/add-writer', methods=['POST'])
  def router_add_writer():
     return add_writer()
  

  # endpoint: login
  @app.route('/login', methods=['POST'])
  def route_login():
     return login()

  

  # endpoint: update profile
  @app.route('/profile-update/<int:id>', methods=['POST'])
  @jwt_required()
  def route_profile_update(id):
     return profile_update(id)

  

  # endpoint: verif writer
  @app.route('/verif-writer/<int:id>', methods=['POST'])
  # @admin_required
  def route_verif_writer(id):
     return verif_writer(id)
  

  # endpoint: create-article
  @app.route('/create-article', methods=['POST'])
  @jwt_required() 
  def route_create_article():
     return create_article()
  

  #endpoint: get-all-article
  @app.route('/get-all-article')
  def route_get_all_article():
     return get_all_article()


  #endpoint: get-article-by-id
  @app.route('/get-article/<int:id>')
  def route_get_article_by_id(id):
     return get_article_by_id(id)
  


  #endpoint: update-article
  @app.route('/update/article/<int:id>', methods=['PUT'])
  @jwt_required()
  def route_update_article(id):
     return update_article(id)
  


  #endpoint: add-viewed-article
  @app.route('/add-viewed/article/<int:id>', methods=['PUT'])
  def route_add_viewed_of_article(id):
     return add_viewed_of_article(id)
  

  #endpoint: delete-article
  @app.route('/article/<int:id>', methods=['DELETE'])
  @jwt_required()
  def route_delete_article(id):
     return delete_article(id)
  

  #endpoint: delete-article
  @app.route('/most-read-article')
  def route_most_read_article():
     return most_read_article()
