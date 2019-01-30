from app import db
from .breeds import Breed


class Dog(db.Model):
    __tablename__ = 'dogs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    breed = db.Column(
        db.Integer, db.ForeignKey(Breed.id, ondelete='cascade'), nullable=False
        )
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float)
    color = db.Column(db.String(256), nullable=False)

    def __init__(self, name, breed, age, weight, color):
        self.name = name
        self.breed = breed
        self.age = age
        self.weight = weight
        self.color = color

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_dog_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all_dogs(cls):
        return cls.query.all()

    @classmethod
    def get_dogs_by_breed(cls, breed_id):
        cls.query.filter_by(breed=breed_id).all()

    @classmethod
    def get_dog_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def calculate_average_age(cls):
        dogs = cls.get_all_dogs()
        return cls.calculate_average_dog_age(dogs)

    @classmethod
    def calculate_average_weight(cls):
        dogs = cls.get_all_dogs()
        return cls.calculate_average_dog_weight(dogs)

    @classmethod
    def calculate_avearge_age_by_breed(cls, breed_id):
        dogs = cls.query.filter_by(breed=breed_id).all()
        return cls.calculate_average_dog_age(dogs)

    @classmethod
    def calculate_average_weight_by_breed(cls, breed_id):
        dogs = cls.query.filter_by(breed=breed_id).all()
        return cls.calculate_average_dog_weight(dogs)
    
    @staticmethod
    def calculate_average_dog_age(collection):
        total = 0
        if len(collection) == 0:
            return 0
        for item in collection:
            total += item.age
        return total/len(collection)

    @staticmethod
    def calculate_average_dog_weight(collection):
        total = 0
        if len(collection) == 0:
            return 0
        for item in collection:
            total += item.weight
        return total/len(collection)

    def __repr__(self):
        return '<Dog {}>'.format(self.name)



