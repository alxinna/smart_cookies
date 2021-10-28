from app import db


class UserScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    test_id = db.Column(db.Integer)
    score = db.Column(db.Integer)