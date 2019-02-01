import json
from .base import BaseTestCase


class TestBreed(BaseTestCase):

    def test_create_breed_success(self):
        with self.client:
            response = self.client.post(
                '/api/v1/breeds',
                data=json.dumps(
                    dict(
                        name="bulldog",
                        description="Guard dog"
                    )
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("bulldog", data["breed"]["name"])
            self.assertIn("Guard dog", data["breed"]["description"])

    def test_create_breed_missing_name(self):
        with self.client:
            response = self.client.post(
                '/api/v1/breeds',
                data=json.dumps(
                    dict(
                        description="Guard dog"
                    )
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                "Missing required parameter",
                data["message"]["name"])

    def test_create_breed_empty_name(self):
        with self.client:
            response = self.client.post(
                '/api/v1/breeds',
                data=json.dumps(
                    dict(
                        name="   ",
                        description="Guard dog"
                    )
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'String should not be empty',
                data['message']['name']
                )

    def test_create_breed_integer_name(self):
        with self.client:
            response = self.client.post(
                '/api/v1/breeds',
                data=json.dumps(
                    dict(
                        name=5,
                        description='dfhdhfd'
                    )
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("String expected", data['message']['name'])

    def test_create_duplicate_breed(self):
        with self.client:
            initial_response = self.client.post(
                '/api/v1/breeds',
                data=json.dumps(
                    dict(
                        name="bulldog",
                        description="Guard dog"
                    )
                ),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/breeds',
                data=json.dumps(
                    dict(
                        name="bulldog",
                        description="another description"
                    )
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(initial_response.status_code, 201)
            self.assertEqual(response.status_code, 409)
            self.assertIn("breed already exists", data["message"])

    def test_get_breeds_list(self):
        with self.client:
            post_breed = self.client.post(
                '/api/v1/breeds',
                data=json.dumps(
                    dict(
                        name="bulldog",
                        description="Guard dog"
                    )
                ),
                content_type='application/json'
            )
            self.assertEqual(post_breed.status_code, 201)

            response = self.client.get(
                '/api/v1/breeds',
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("bulldog", data["breeds"][0]["name"])
            self.assertIn("Guard dog", data["breeds"][0]["description"])

    def test_get_single_breed(self):
        with self.client:
            post_breed = self.client.post(
                '/api/v1/breeds',
                data=json.dumps(
                    dict(
                        name="bulldog",
                        description="Guard dog"
                    )
                ),
                content_type='application/json'
            )
            self.assertEqual(post_breed.status_code, 201)

            response = self.client.get(
                '/api/v1/breeds/1',
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("bulldog", data["breed"]["name"])
            self.assertIn("Guard dog", data["breed"]["description"])

    def test_get_single_breed_invalid_id(self):
        with self.client:
            post_breed = self.client.post(
                '/api/v1/breeds',
                data=json.dumps(
                    dict(
                        name="bulldog",
                        description="Guard dog"
                    )
                ),
                content_type='application/json'
            )
            self.assertEqual(post_breed.status_code, 201)

            response = self.client.get(
                '/api/v1/breeds/2',
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn(
                "Breed with provided id does not exist",
                data["message"])

    def test_delete_breed_success(self):
        with self.client:
            post_breed = self.client.post(
                '/api/v1/breeds',
                data=json.dumps(
                    dict(
                        name="bulldog",
                        description="Guard dog"
                    )
                ),
                content_type='application/json'
            )
            self.assertEqual(post_breed.status_code, 201)
            delete_breed = self.client.delete(
                '/api/v1/breeds/1',
                content_type='application/json'
            )
            data = json.loads(delete_breed.data.decode())
            self.assertEqual(delete_breed.status_code, 200)
            self.assertIn("Breed deleted", data["message"])
            get_breed = self.client.get(
                '/api/v1/breeds/1',
                content_type='application/json'
            )
            self.assertEqual(get_breed.status_code, 404)

    def test_delete_breed_invalid_id(self):
        with self.client:
            delete_breed = self.client.delete(
                '/api/v1/breeds/1',
                content_type='application/json'
            )
            data = json.loads(delete_breed.data.decode())
            self.assertEqual(delete_breed.status_code, 404)
            self.assertIn(
                "Breed with provided id does not exist",
                data["message"]
                )

    def test_update_breed_invalid_id(self):
        with self.client:
            response = self.client.put(
                '/api/v1/breeds/1',
                data=json.dumps(
                    dict(
                        name="local",
                        description="native breeds"
                    )
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn(
                "Breed with provided id does not exist",
                data["message"]
                )

    def test_update_breed_success(self):
        with self.client:
            post_breed = self.client.post(
                '/api/v1/breeds',
                data=json.dumps(
                    dict(
                        name="bulldog",
                        description="Guard dog"
                    )
                ),
                content_type='application/json'
            )
            self.assertEqual(post_breed.status_code, 201)
            put_breed = self.client.put(
                '/api/v1/breeds/1',
                data=json.dumps(
                    dict(
                        name="local",
                        description="native breeds"
                    )
                ),
                content_type='application/json'
            )
            data = json.loads(put_breed.data.decode())
            self.assertEqual(put_breed.status_code, 200)
            self.assertIn("local", data["breed"]["name"])
            self.assertIn("native breeds", data["breed"]["description"])

    def test_update_breed_to_duplicate_name(self):
        with self.client:
            post_breed = self.client.post(
                '/api/v1/breeds',
                data=json.dumps(
                    dict(
                        name="bulldog",
                        description="Guard dog"
                    )
                ),
                content_type='application/json'
            )
            post_breed_2 = self.client.post(
                '/api/v1/breeds',
                data=json.dumps(
                    dict(
                        name="german shepherd",
                        description="Guard dog"
                    )
                ),
                content_type='application/json'
            )
            self.assertEqual(post_breed.status_code, 201)
            self.assertEqual(post_breed_2.status_code, 201)
            put_breed = self.client.put(
                '/api/v1/breeds/1',
                data=json.dumps(
                    dict(
                        name="german shepherd",
                        description="Tough and tall"
                    )
                ),
                content_type='application/json'
            )
            data = json.loads(put_breed.data.decode())
            self.assertEqual(put_breed.status_code, 409)
            self.assertIn(
                "Breed with specified name already exist",
                data["message"]
                )


            
