"""
Test for recipe API.
"""



from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPE_URL = None
RECIPES_URL = None
def create_recipe(user, **params):
    """Create and return a sample recipe."""
    
    defaults = {
        'title':'Sample recipe title',
        'times_minutes':22,
        'price': Decimal('15.52'),
        'description': 'Sample description',
        'link': 'google.pl'
    }
    
    defaults.update(params)
    
    recipe = Recipe.objects.create(user = user, **defaults)
    return Recipe


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""
    
    def setUp(self):
        self.client = APIClient()
        
    def test_auth_required(self):
        """Testing whether auth is required to call API."""
        res = self.client.get(RECIPE_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    

class PrivateRecipeAPITests(TestCase):
    """Test authenticated API requests"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "sample@example.com",
            "samplepassword123")
        
    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_recipe(self.user)
        create_recipe(self.user, {'title':'Sample recipe 2'})
        
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many = True)
        self.assertEqual(res.data, serializer.data)
        
    def test_recipe_list_limited_to_use(self):
        """Test if list of recipes is limited only to the authenticated user."""
        other_user_data = [
            "sampl22e@example.com",
            "samplepassword123"]        
        other_user = get_user_model().objects.create_user(other_user_data)
        
        create_recipe(self.user)
        create_recipe(other_user)
        
        res = self.client.get(RECIPES_URL)
        
        recipes_self_user = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes_self_user, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)