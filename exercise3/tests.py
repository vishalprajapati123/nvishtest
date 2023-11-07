import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import KeyValue

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_save_key_value_pair(api_client):
    url = reverse('save')
    data = {'key': 'testkey', 'value': 'testvalue'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert KeyValue.objects.filter(key='testkey').exists()

@pytest.mark.django_db
def test_save_without_key_or_value(api_client):
    url = reverse('save')
    # Test without key
    data = {'value': 'testvalue'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Test without value
    data = {'key': 'testkey'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_get_existing_key(api_client):
    KeyValue.objects.create(key='existingkey', value='existingvalue')
    url = reverse('get_value') + '?key=existingkey' 
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['key'] == 'existingkey'
    assert response.data['value'] == 'existingvalue'

@pytest.mark.django_db
def test_get_non_existing_key(api_client):
    url = reverse('get_value') + '?key=end2endkey' 
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_end_to_end_save_and_retrieve(api_client):
    # Save a new key-value pair
    save_url = reverse('save')
    data = {'key': 'end2endkey', 'value': 'end2endvalue'}
    save_response = api_client.post(save_url, data=data, format='json')
    assert save_response.status_code == status.HTTP_201_CREATED

    # Retrieve the newly saved key-value pair
    url = reverse('get_value') + '?key=end2endkey' 
    get_response = api_client.get(url)
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.data == {'key': 'end2endkey', 'value': 'end2endvalue'}
