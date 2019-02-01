from flask import Blueprint
from flask_restful import (
    Resource, reqparse, Api, marshal,
    fields
    )

from models.dogs import Dog
from validations import non_empty_string

dog_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'breed': fields.Integer,
    'age': fields.Integer,
    'weight': fields.Float,
    'color': fields.String
}


class DogList(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            type=non_empty_string,
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'breed',
            type=int,
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'age',
            type=int,
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'weight',
            type=float,
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'color',
            type=non_empty_string,
            required=True,
            location=['form', 'json']
        )
        super().__init__()

    def post(self):

        args = self.reqparse.parse_args()
        name = args.get('name')

        existing_dog = Dog.get_dog_by_name(name)

        if not existing_dog:
            try:
                new_dog = Dog(**args)
                new_dog.save()
                return {'dog': marshal(new_dog, dog_fields)}, 201
            except Exception as e:
                return {'message': str(e)}, 400
        return {'message': 'Dog with specified name already exists'}, 409

    def get(self):
        return {'dogs': [
            marshal(dog, dog_fields)
            for dog in Dog.get_all_dogs()
        ]}


class DogResource(Resource):

    def get(self, id):
        dog = Dog.get_dog_by_id(id)

        if dog:
            return {'dog': marshal(dog, dog_fields)}, 200
        return {'message': 'Dog with provided id does not exist'}, 404

    def delete(self, id):
        dog_to_delete = Dog.get_dog_by_id(id)

        if not dog_to_delete:
            return {'message': 'Dog with specified id does not exist'}, 404

        dog_to_delete.delete()
        return {'message': 'Dog deleted'}, 200


dogs_api = Blueprint('resources.dogs', __name__)
api = Api(dogs_api, catch_all_404s=True)
api.add_resource(
    DogList,
    '',
    endpoint='dogs'
)
api.add_resource(
    DogResource,
    '/<int:id>',
    endpoint='dog'
)
