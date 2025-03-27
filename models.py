from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    last_score = db.Column(db.Integer, default=0)
    high_score = db.Column(db.Integer, default=0)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    correct_answer = db.Column(db.String(100))
    options = db.Column(db.PickleType)  # ['a', 'b', 'c', 'd']
