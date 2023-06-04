"""
Tests for models.
"""

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

test_email = 'test@example.com'
test_password = 'testpass123'
class ModelTests(TestCase):
    """Test models."""
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        user = get_user_model().objects.create_user(
            email=test_email,
            password=test_password,
        )

        self.assertEqual(user.email, test_email)
        self.assertTrue(user.check_password(test_password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)
            
            
            
    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email address raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', test_password)
        
        
    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(test_email, test_password)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        
    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(test_email, test_password)

        recipe = models.Recipe.objects.create(
            user = user,
            title = 'Sample recipe name',
            time_minutes = 5,
            price = Decimal('5.50'),
            description = 'Sample recipe desc'
        )
        self.assertEqual(str(recipe), recipe.title)