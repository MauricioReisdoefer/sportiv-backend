from util import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    state = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
