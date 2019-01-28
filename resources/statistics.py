from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from models.dogs import Dog


class DogStatistics(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'breed',
            type=int,
            required=False
        )

    def get(self):
        args = self.reqparse.parse_args()

        breed_id = args.get('breed')

        if breed_id is None:
            average_weight = Dog.calculate_average_weight()
            average_age = Dog.calculate_average_age()
        else:
            average_weight = Dog.calculate_average_weight_by_breed(breed_id)
            average_age = Dog.calculate_avearge_age_by_breed(breed_id)

        return {
                "statistics": {
                    "average_weight": average_weight,
                    "average_age": average_age
                }
            }, 200

stats_api = Blueprint('resources.statistics', __name__)
api = Api(stats_api, catch_all_404s=True)
api.add_resource(
    DogStatistics,
    '',
    endpoint='stats'
)