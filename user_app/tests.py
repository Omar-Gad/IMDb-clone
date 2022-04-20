from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase


class RegisterTestCase(APITestCase):
    """Test case for user registration"""
    def test_register(self):
        data = {
            'username': 'testcase',
            'email': 'testcase@exapmle.com',
            'password': 'NewPassword@123',
            'password2': 'NewPassword@123'
        }
        response = self.client.post(reverse('register'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase):
    """Test case for login"""
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='123'
        )

    def test_login(self):
        data = {
            'username': 'test',
            'password': '123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        