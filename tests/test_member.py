from application import create_app
from application.models import db, Member
import unittest
from werkzeug.security import generate_password_hash

from application.utils.util import encode_token


class MemberRoutes(unittest.TestCase):

    def setUp(self):
        #Sets up test client
        self.app = create_app("TestingConfig")
        self.member = Member(name="Tester", email="Test@test.com", phone="1234567890", password=generate_password_hash("test"), role="admin")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.member)
            db.session.commit()
        self.client = self.app.test_client()
        self.token = encode_token(1, "admin")

    def test_create_member(self):
        new_member = {
            "name": "Dylan",
            "email": "dk@email.com",
            "phone": "123-456-7890",
            "password": "123",
            "role": "admin"
        }
        response = self.client.post('/members/', json=new_member)
        print(response.json)
        self.assertEqual(response.status_code, 201)

    def test_unique_member(self):
        new_member = {
            "name": "Tester`",
            "email": "Test@test.com",
            "phone": "123-456-7890",
            "password": "test",
            "role": "admin"
        }
        response = self.client.post('/members/', json=new_member)
        print(response.json)
        self.assertEqual(response.status_code, 400)
    
    def test_login_user(self):
        credentials = {
            "email": "Test@test.com",
            "password": "test"
        }

        response = self.client.post('/members/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']
    
    def test_delete_user(self):
        headers = {'Authorization': "Bearer " + self.token}

        response = self.client.delete('/members/', headers=headers)
        self.assertEqual(response.status_code, 200)

