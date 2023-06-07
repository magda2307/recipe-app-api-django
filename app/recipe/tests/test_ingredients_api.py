"""
Tests for the ingredients API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')

def detail_url(ingredient_id):
    """Create and return a ingredient detail URL."""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])
    

def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicIngredientApiTests(TestCase):
    """Test unauthorized API requests."""

    def setUp(self):
        self.client = APIClient()  
        
    def test_auth_required(self):
        """Test checking required authentication."""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        


class PrivateIngredientsApiTests(TestCase):
    """Test authorized API requests."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)
    
    def test_retrieveIngredients(self):
        Ingredient.objects.create(user=self.user, name='Apple')
        Ingredient.objects.create(user=self.user, name = 'Celery')
        
        res = self.client.get(INGREDIENTS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        all_ingredients = Ingredient.object.all().order_by('-name')
        serializer = IngredientSerializer(all_ingredients, many=True)
        self.assertEqual(res.content, serializer.data)
    
    def test_ingredients_limited_to_user(self):
        """Test ingredients limited to an user."""
        user2 = create_user(email = 'user2@example.com')
        ingredient2 = Ingredient.objects.create(user=user2, name='salt')
        ingredient = Ingredient.objects.create(user = self.user, name='Pepper')
        
        res = self.client.get(INGREDIENTS_URL)
        
        self.assertTrue(res.data[0]['name'], ingredient.name)
        self.assertNotIn(res.content, ingredient2)
        self.assertTrue(res.status_code, status.HTTP_200_OK)
        