from app import db
from flask import request, jsonify
from models.articles import Articles
from flask_jwt_extended import get_jwt_identity

# logic: create article
def create_article():
  data = request.get_json()
  title = data.get('title')
  sub_title = data.get('sub_title')
  body = data.get('body')
  viewed = 0
  created_at = data.get('created_at')
  user = get_jwt_identity()

  new_artilce = Articles(title=title, sub_title=sub_title, body=body, viewed=viewed, created_at=created_at, writer_id=user['id'])
  db.session.add(new_artilce)
  db.session.commit()

  return jsonify({'message': 'created'}),201


# logic: get all article
def get_all_article():
  articles = Articles.query.paginate()
  return jsonify({'total': articles.total,
                  'data': [{ 'title': article.title, 
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
    'title': article.title,
    'sub_title': article.sub_title,
    'body': article.body,
    'viewed': article.viewed,
    'created_at': article.created_at,
    'writer': article.user.name
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

