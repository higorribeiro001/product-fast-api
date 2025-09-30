from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.utils.sql_alchemy import db

class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(220), nullable=False)
    mark = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, name, mark, value):
        self.name = name
        self.mark = mark
        self.value = value

    def json(self):
        return {
            "id": str(self.id),
            'name': self.name, 
            'mark': self.mark, 
            'value': self.value, 
        }
    
    @classmethod
    def find_product(cls, id):
        product = cls.query.filter_by(id=id).first()
        if product:
            return product
        return None

    def save_product(self):
        db.session.add(self)
        db.session.commit()

    def update_product(self, name, mark, value):
        self.name = name
        self.mark = mark
        self.value = value

    def delete_product(self):
        db.session.delete(self)
        db.session.commit()