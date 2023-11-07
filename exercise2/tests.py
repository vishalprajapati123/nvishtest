import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='normal_user', password='testpass123')

@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(username='super_user', password='testpass123')

@pytest.fixture
def get_or_create_token(db, superuser):
    token, created = Token.objects.get_or_create(user=superuser)
    return token

# Test for AuthorizeView
@pytest.mark.django_db
def test_authorize_view_success(api_client, superuser, get_or_create_token):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_or_create_token.key)
    url = reverse('authorize')
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['user'] == superuser.username

@pytest.mark.django_db
def test_authorize_view_failure(api_client):
    url = reverse('authorize')
    response = api_client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


