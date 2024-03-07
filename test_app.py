import unittest
from app import app, UserService

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        UserService.users = {}
        UserService.current_id = 1

    def test_create_user(self):
        response = self.app.post('/users', json={
            'firstName': 'John',
            'lastName': 'Doe',
            'birthYear': 1990,
            'group': 'user'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], 1)

    def test_get_user_not_found(self):
        response = self.app.get('/users/999')
        self.assertEqual(response.status_code, 404)

    def test_create_user_invalid_group(self):
        response = self.app.post('/users', json={
            'firstName': 'Jane',
            'lastName': 'Doe',
            'birthYear': 1995,
            'group': 'unknown'
        })
        self.assertEqual(response.status_code, 400)

    def test_delete_user(self):
        self.app.post('/users', json={
            'firstName': 'Delete',
            'lastName': 'Me',
            'birthYear': 1990,
            'group': 'user'
        })
        del_response = self.app.delete('/users/1')
        self.assertEqual(del_response.status_code, 204)
        get_response = self.app.get('/users/1')
        self.assertEqual(get_response.status_code, 404)
    def test_update_user(self):
        create_response = self.app.post('/users', json={
            'firstName': 'Update',
            'lastName': 'Me',
            'birthYear': 1990,
            'group': 'user'
        })
        self.assertEqual(create_response.status_code, 201)
        user_id = create_response.json['id']

        update_response = self.app.patch(f'/users/{user_id}', json={
            'firstName': 'Updated',
            'lastName': 'Successfully'
        })
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json['firstName'], 'Updated')
        self.assertEqual(update_response.json['lastName'], 'Successfully')

        get_response = self.app.get(f'/users/{user_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json['firstName'], 'Updated')
        self.assertEqual(get_response.json['lastName'], 'Successfully')

if __name__ == '__main__':
    unittest.main()