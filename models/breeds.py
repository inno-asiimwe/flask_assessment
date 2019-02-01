from app import db


class Breed(db.Model):
    __tablename__ = 'breeds'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    name_to_compare = db.Column(db.String(256), nullable=False, unique=True)
    description = db.Column(db.String(256))
    dogs = db.relationship(
        'Dog',
        backref='Dog',
        cascade='all, delete-orphan'
    )

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.name_to_compare = ''.join(name.lower().strip().split())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_breed_by_name(cls, name):
        name_to_compare = ''.join(name.lower().strip().split())
        return cls.query.filter_by(name_to_compare=name_to_compare).first()

    @classmethod
    def get_all_breeds(cls):
        return cls.query.all()

    @classmethod
    def get_breed_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def __repr__(self):
        return '<Breed {}>'.format(self.name)
