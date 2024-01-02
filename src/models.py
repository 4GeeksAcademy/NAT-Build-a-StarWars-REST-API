from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_favorite = db.relationship("Favorite", backref="user", uselist=True)


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "created": self.created
            # do not serialize the password, its a security breach
        }
    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)

    def __repr__(self):
        return '<Favorite %>' % self.id
    
    def serialize(self):
        return {
            "id": self.user_id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db. Column(db.String(120), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String, nullable=False )
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    planets_favorite =db.relationship("Favorite", backref="planets", uselist=True)

    def __repr__(self):
        return '<Planets %>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "created": self.created
        }
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)    
    age = db.Column(db.Integer, unique=False, nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    people_favorite = db.relationship("Favorite", backref="people", uselist=True)
    
    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "created": self.created
        }
