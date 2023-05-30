"""
Urls mappings for the user API.
"""


from django.urls import path

from user import views

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create')
]
