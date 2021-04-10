from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    __tablename__:'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    def __repr__(self):
        return '<Person %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "age":self.age
        }

class PeopleRelationship(db.Model):
    __tablename__='PeopleRelationship'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer,db.ForeignKey('person.id'),nullable=False)
    father_id = db.Column(db.Integer,db.ForeignKey('person.id'),nullable=True)
    mother_id = db.Column(db.Integer,db.ForeignKey('person.id'),nullable=True)

    def __repr__(self):
        return '<PeopleRelationship %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "person_id": self.person_id,
            "father_id": self.father_id,
            "mother_id":self.mother_id
        }