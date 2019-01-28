import json
from .base import BaseTestCase


class TestDog(BaseTestCase):

    def post_a_breed(self, name='bulldog', description='Guard dog'):
        response = self.client.post(
            '/api/v1/breeds',
            data=json.dumps({
                "name": name,
                "description": description
            }),
            content_type='application/json'
        )
        return response

    def test_create_dog_success(self):
        with self.client:
            post_breed = self.post_a_breed()
            response = self.client.post(
                '/api/v1/dogs',
                data=json.dumps(
                    dict(
                        name="fox",
                        breeds=[1],
                        age=12,
                        weight=25.6,
                        color="black"
                    )
                ),
                content_type='application/json'
            )
            self.assertEqual(post_breed.status_code, 201)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("fox", data["dog"]["name"])
            self.assertIn("black", data["dog"]["color"])

    def test_create_dog_duplicate_name(self):
        with self.client:
            post_breed = self.post_a_breed()
            response = self.client.post(
                '/api/v1/dogs',
                data=json.dumps(
                    dict(
                        name="fox",
                        breeds=[1],
                        age=12,
                        weight=25.6,
                        color="black"
                    )
                ),
                content_type='application/json'
            )
            duplicate = self.client.post(
                '/api/v1/dogs',
                data=json.dumps(
                    dict(
                        name="fox",
                        breeds=[1],
                        age=12,
                        weight=25.6,
                        color="black"
                    )
                ),
                content_type='application/json'
            )
            self.assertEqual(post_breed.status_code, 201)
            self.assertEqual(response.status_code, 201)
            data = json.loads(duplicate.data.decode())
            self.assertEqual(duplicate.status_code, 409)
            self.assertIn(
                "Dog with specified name already exists",
                data["message"]
                )

    def test_get_dog_list(self):
        with self.client:
            post_breed = self.post_a_breed()
            post_dog = self.client.post(
                '/api/v1/dogs',
                data=json.dumps(
                    dict(
                        name="fox",
                        breeds=[1],
                        age=12,
                        weight=25.6,
                        color="black"
                    )
                ),
                content_type='application/json'
            )
            self.assertEqual(post_breed.status_code, 201)
            self.assertEqual(post_dog.status_code, 201)
            
            response = self.client.get(
                '/api/v1/dogs',
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("fox", data["dogs"][0]["name"])
            self.assertEqual(12, data["dogs"][0]["age"])

    def test_get_single_dog_success(self):
        with self.client:
            post_breed = self.post_a_breed()
            post_dog = self.client.post(
                '/api/v1/dogs',
                data=json.dumps(
                    dict(
                        name="fox",
                        breeds=[1],
                        age=12,
                        weight=25.6,
                        color="black"
                    )
                ),
                content_type='application/json'
            )
            self.assertEqual(post_breed.status_code, 201)
            self.assertEqual(post_dog.status_code, 201)

            response = self.client.get(
                '/api/v1/dogs/1',
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("fox", data["dog"]["name"])
            self.assertIn("black", data["dog"]["color"])
            self.assertEqual(12, data["dog"]["age"])
            self.assertEqual(25.6, data["dog"]["weight"])

    def test_get_single_dog_invalid_id(self):
        with self.client:
            response = self.client.get(
                '/api/v1/dogs/2',
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn(
                "Dog with provided id does not exist",
                data["message"])

    def test_delete_dog_success(self):
        with self.client:
            post_breed = self.post_a_breed()
            post_dog = self.client.post(
                '/api/v1/dogs',
                data=json.dumps(
                    dict(
                        name="fox",
                        breeds=[1],
                        age=12,
                        weight=25.6,
                        color="black"
                    )
                ),
                content_type='application/json'
            )
            self.assertEqual(post_breed.status_code, 201)
            self.assertEqual(post_dog.status_code, 201)

            response = self.client.delete(
                '/api/v1/dogs/1',
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(200, response.status_code)
            self.assertIn('Dog deleted', data["message"])

    def test_delete_dog_invalid_id(self):
        with self.client:
            response = self.client.delete(
                '/api/v1/dogs/2',
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(404, response.status_code)
            self.assertIn('id does not exist', data["message"])

