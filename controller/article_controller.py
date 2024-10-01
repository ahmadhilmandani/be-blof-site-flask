from app import db
from flask import request, jsonify
from models.articles import Articles
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import desc
import pyimgur
import os
from werkzeug.utils import secure_filename

# logic: create article
def create_article():
  title = request.form.get('title')
  sub_title = request.form.get('sub_title')
  body = request.form.get('body')
  viewed = 0
  created_at = request.form.get('created_at')
  user = get_jwt_identity()

  if 'image' not in request.files:
    return jsonify({'error': 'No image file in the request'}), 400
    
  image = request.files['image']

  UPLOAD_FOLDER = 'uploads'
  os.makedirs(UPLOAD_FOLDER, exist_ok=True)
  filename = secure_filename(image.filename)
  filepath = os.path.join(UPLOAD_FOLDER, filename)
  image.save(filepath)

  im = pyimgur.Imgur('9e1bf0fda6cb5ad')

  try:
    uploaded_image = im.upload_image(filepath, title="test")
    os.remove(filepath)
  except Exception as e:
    return jsonify({"error": str(e)}), 500


  new_artilce = Articles(title=title, sub_title=sub_title, body=body, viewed=viewed, created_at=created_at, writer_id=user['id'], thumbnail_url=uploaded_image.link)
  db.session.add(new_artilce)
  db.session.commit()

  return jsonify({'message': 'created'}),201


# logic: get all article
def get_all_article():
  articles = Articles.query.paginate()
  return jsonify({'total': articles.total,
                  'data': [{ 'id':article.id, 'title': article.title, 
                  'sub_title': article.sub_title, 
                  'body': article.body, 
                  'viewed': article.viewed, 
                  'created_at': article.created_at, 
                  'writer': article.user.name 
                  } for article in articles.items]
                }), 200


#logic: get article by id
def get_article_by_id(id):
  article = Articles.query.filter_by(id=id).first()
  return jsonify({
    'id': id,
    'title': article.title,
    'sub_title': article.sub_title,
    'body': article.body,
    'viewed': article.viewed,
    'created_at': article.created_at,
    'writer': article.user.name
  }), 200


#logic: get most read
def most_read_article():
  articles =  Articles.query.order_by(desc(Articles.viewed)).paginate(page=1, per_page=5)
  return jsonify({'total': articles.total,
                  'data': [{ 'title': article.title, 
                  'sub_title': article.sub_title, 
                  'body': article.body, 
                  'viewed': article.viewed, 
                  'created_at': article.created_at, 
                  'writer': article.user.name 
                  } for article in articles.items]
                }), 200


#logic: update article
def update_article(id):
  article = Articles.query.filter_by(id=id).first()
  user = get_jwt_identity()

  if user['id'] != article.writer_id:
    return jsonify(msg="Unauth"), 401
  
  data = request.get_json()
  article.title = data.get('title')
  article.sub_title = data.get('sub_title')
  article.body = data.get('body')

  db.session.commit()
  
  return jsonify({
    'title': article.title,
    'sub_title': article.sub_title,
    'body': article.body,
    'viewed': article.viewed,
    'created_at': article.created_at,
    'writer': article.user.name
  }), 200



#logic: delete article
def delete_article(id):
  user = get_jwt_identity()
  article = Articles.query.get_or_404(id)
  
  if user['id'] != article.writer_id or user['role'] == 'admin':
    return jsonify(msg="Unauth"), 401
  
  db.session.delete(article)
  db.session.commit()

  return jsonify({'message': 'article deleted'}), 200




#logic: add viewed in article
def add_viewed_of_article(id):
  article = Articles.query.filter_by(id=id).first()
  
  article.viewed += 1

  db.session.commit()

  return jsonify({
    'title': article.title,
    'sub_title': article.sub_title,
    'body': article.body,
    'viewed': article.viewed,
    'created_at': article.created_at,
    'writer': article.user.name
  }), 200

