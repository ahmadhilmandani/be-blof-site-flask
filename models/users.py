from app import db

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  is_verif = db.Column(db.Boolean, nullable=False, default=False)
  role = db.Column(db.String(50), nullable=False, default='writter')
  password = db.Column(db.String(128), nullable=False)
  short_bio = db.Column(db.Text(), nullable=True)
  
  article = db.relationship('Articles', backref='user', lazy=True)
  def __repr__(self):
    return f'user: {self.name}'