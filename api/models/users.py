from ..utils import db


class User(db.Model):
    __tablename__= "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(),unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password_hash = db.Column(db.Text(),nullable=False)
    is_staff = db.Column(db.Boolean(), default=False)
    is_active = db.Column(db.Boolean(), default=False)
    orders = db.relationship("Order", backref='User', lazy=True)
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        


    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
