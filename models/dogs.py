from app import db
from .breeds import Breed


class Dog(db.Model):
    __tablename__ = 'dogs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    name_to_compare = db.Column(db.String(256), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float)
    color = db.Column(db.String(256), nullable=False)
    breeds = db.relationship(
        'Breed', secondary='dog_breeds', backref=db.backref('dogs')
        )

    def __init__(self, name, age, weight, color):
        self.name = name
        self.name_to_compare = ''.join(name.lower().strip().split())
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
        name_to_compare = ''.join(name.lower().strip().split())
        return cls.query.filter_by(name_to_compare=name_to_compare).first()

    @classmethod
    def get_all_dogs(cls):
        return cls.query.all()

    @classmethod
    def get_dogs_by_breed(cls, breed_id):
        breed = Breed.get_breed_by_id(breed_id)
        all_dogs = cls.get_all_dogs()
        return [dog for dog in all_dogs if breed in dog.breeds]

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
        dogs = cls.get_dogs_by_breed(breed_id)
        return cls.calculate_average_dog_age(dogs)

    @classmethod
    def calculate_average_weight_by_breed(cls, breed_id):
        dogs = cls.get_dogs_by_breed(breed_id)
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


class DogBreeds(db.Model):
    __tablename__ = 'dog_breeds'
    breed_id = db.Column(db.Integer, db.ForeignKey(Breed.id), primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey(Dog.id), primary_key=True)

    def __init__(self, dog_id, breed_id):
        self.dog_id = dog_id
        self.breed_id = breed_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit(self)
