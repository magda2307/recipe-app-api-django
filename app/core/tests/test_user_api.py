"""
Tests for the user API.
"""


from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

TOKEN_URL = reverse('user:token')

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public (no authentication) features of the user API."""
    
    def setUp(self):
        self.client = Client()
        
        
    def test_create_user_success(self):
        """Test if creating an user is successful."""
        payload = {
        'email': 'test@example.com',
        'password':'testpass123',
        'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email = payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)
        
        
    def test_user_with_email_exists_error(self):
        """Test error returned if user with this email already exists."""
        payload = {
        'email': 'test@example.com',
        'password':'testpass123',
        'name': 'Test Name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_user_with_too_short_password(self):
        """Test error returned if attempt of creating an user with too short password."""
        payload = {
        'email': 'test123@example.com',
        'password':'tes1',
        'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
            ).exists()
        self.assertFalse(user_exists)
        
    def test_create_token_for_user(self):
        """Test generate token for valid user credentials."""
        user_details = {
        'email' : 'test@example.com',
        'password' : 'password1234',
        }
        create_user(**user_details)
        res = self.client.post(TOKEN_URL, user_details)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)
        
    def test_create_token_bad_credentials(self):
        """Test generate token for valid user credentials."""
        user_details = {
        'email' : 'test@example.com',
        'password' : 'password1234',
        }
        bad_user_details = {
        'email' : 'test@example.com',
        'password' : 'wrong_pass',
        }
        create_user(**user_details)
        res = self.client.post(TOKEN_URL, bad_user_details)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
        
    def test_create_token_blank_password(self):
        """Test generate token for blank password in user credentials."""
        bad_user_details = {
        'email' : 'test@example.com',
        'password' : '',
        }
        res = self.client.post(TOKEN_URL, bad_user_details)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
        