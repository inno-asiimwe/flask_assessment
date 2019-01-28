from flask import Blueprint
from flask_restful import (
    Resource, reqparse, Api, marshal,
    fields
    )

from models.breeds import Breed

breed_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}


class BreedList(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            type=str,
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'description',
            type=str,
            required=False,
            location=['form', 'json']
        )
        super().__init__()

    def post(self):

        args = self.reqparse.parse_args()
        name = args.get('name')

        existing_breed = Breed.get_breed_by_name(name)

        if not existing_breed:
            breed = Breed(**args)
            breed.save()
            return {'breed': marshal(breed, breed_fields)}, 201
        return {'message': 'breed already exists'}, 409

    def get(self):
        all_breeds = Breed.get_all_breeds()

        return {'breeds': [marshal(breed, breed_fields)
                           for breed in all_breeds]}, 200


class BreedResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            type=str,
            required=False,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'description',
            type=str,
            required=False,
            location=['form', 'json']
        )
        super().__init__()

    def get(self, id):
        breed = Breed.get_breed_by_id(id)

        if breed:
            return {'breed': marshal(breed, breed_fields)}, 200
        return {'message': 'Breed with provided id does not exist'}, 404

    def put(self, id):
        args = self.reqparse.parse_args()
        name = args.get('name')
        description = args.get('description')
        breed = Breed.get_breed_by_id(id)

        if not breed:
            return {'message': 'Breed with provided id does not exist'}, 404

        if not args:
            return {'messgae': 'No update data'}, 400

        if name != breed.name and Breed.get_breed_by_name(name):
            return {'message': 'Breed with specified name already exist'}, 409

        if name != breed.name:
            breed.name = name
        
        if description != breed.description:
            breed.description = description

        breed.save()
        return {'breed': marshal(breed, breed_fields)}, 200

    def delete(self, id):
        breed = Breed.get_breed_by_id(id)

        if not breed:
            return {'message': 'Breed with provided id does not exist'}, 404

        breed.delete()
        return {'message': "Breed deleted"}, 200


breeds_api = Blueprint('resources.breeds', __name__)
api = Api(breeds_api, catch_all_404s=True)
api.add_resource(
    BreedList,
    '',
    endpoint='breeds'
)
api.add_resource(
    BreedResource,
    '/<int:id>',
    endpoint='breed'
)
