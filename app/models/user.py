from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.utils.sql_alchemy import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(220), nullable=False)
    email = db.Column(db.String(220), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def json(self):
        return {
            'id': str(self.id),
            'name': self.name, 
            'email': self.email, 
        }
    
    @classmethod
    def find_user(cls, id):
        user = cls.query.filter_by(id=id).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_login(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()