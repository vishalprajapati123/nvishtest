import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from exercise3.models import *

# Setup a fixture for the API client
@pytest.fixture
def api_client():
    return APIClient()

# Unit tests
@pytest.mark.django_db
class TestSaveView:
    def test_save_key_value_pair(self, api_client):
        url = reverse('cashesave')  # Make sure 'save' is the correct name for your URL
        data = {'key': 'testkey', 'value': 'testvalue'}
        response = api_client.post(url, data=data, format='json')  # Added format='json'
        assert response.status_code == status.HTTP_201_CREATED
        assert KeyValue.objects.filter(key='testkey').exists()

    def test_save_without_key_or_value(self, api_client):
        url = reverse('save')  # Make sure 'save' is the correct name for your URL
        # Testing without key
        data = {'value': 'testvalue'}
        response = api_client.post(url, data, format='json')  # Added format='json'
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # Testing without value
        data = {'key': 'testkey'}
        response = api_client.post(url, data, format='json')  # Added format='json'
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestGetView:
    def test_get_existing_key(self, api_client):
        KeyValue.objects.create(key='existingkey', value='existingvalue')
        url = reverse('casheget', kwargs={'key': 'existingkey'})  # Assuming your URL name is 'casheget'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'key': 'existingkey', 'value': 'existingvalue'}

    def test_get_non_existing_key(self, api_client):
        url = reverse('casheget', kwargs={'key': 'nonexistingkey'})  # Assuming your URL name is 'casheget'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestKeyValueEndToEnd:
    def test_save_and_retrieve_key_value(self, api_client):
        # Save a new key-value pair
        save_url = reverse('save')  # Make sure 'save' is the correct name for your URL
        data = {'key': 'e2ekey', 'value': 'e2evalue'}
        save_response = api_client.post(save_url, data, format='json')  # Added format='json'
        assert save_response.status_code == status.HTTP_201_CREATED

        # Retrieve the key-value pair
        get_url = reverse('casheget', kwargs={'key': 'e2ekey'})  # Assuming your URL name is 'casheget'
        get_response = api_client.get(get_url)
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json() == {'key': 'e2ekey', 'value': 'e2evalue'}
