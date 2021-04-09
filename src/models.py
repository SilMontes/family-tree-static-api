from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    date_of_birth = db.Column(db.Date, unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    father_id = db.Column(db.Integer, unique=False,nullable=True)
    mother_id = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "date_of_birth":self.date_of_birth,
            "age":self.age,
            "father_id": self.father_id,
            "mother_id": self.mother_id
            # do not serialize the password, its a security breach
        }