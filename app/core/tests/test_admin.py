"""
Tests for Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""
    
    def setUp(self):
        """Create user and client."""
        self.client = Client()
        
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password = 'password123',
            name = 'Test user'
            )
        
    def test_users_list(self):
        """Test whether the users are listed on page."""
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)