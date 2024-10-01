from app import db

class Articles(db.Model):
  __tablename__ = 'article'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  sub_title = db.Column(db.String(255), nullable=False)
  body = db.Column(db.Text(), nullable=False)
  viewed = db.Column(db.Integer, default=0)
  created_at = db.Column(db.TIMESTAMP)
  thumbnail_url = db.Column(db.Text(), nullable=False)
  writer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  def __repr__(self):
    return f'user: {self.name}'