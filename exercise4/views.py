# views.py

from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from exercise3.models import KeyValue
from rest_framework.response import Response

# Helper functions
def get_from_cache(key):
    """Retrieve a value from the cache."""
    return cache.get(f'kv_{key}')

def save_to_cache(key, value):
    """Save a value to the cache."""
    cache_key = f'kv_{key}'
    cache.set(cache_key, value)

def get_from_db(key):
    """Retrieve a value from the database."""
    try:
        kv_object = KeyValue.objects.get(key=key)
        # Save to cache before returning
        save_to_cache(key, kv_object.value)
        return kv_object.value
    except KeyValue.DoesNotExist:
        return None

@method_decorator(csrf_exempt, name='dispatch')
class SaveViewCashe(APIView):
    def post(self, request, *args, **kwargs):
        key = request.data['key']
        value = request.data['value']

        if not key or not value:
            return Response({'error': 'Key and value are required.'}, status=400)
        
        KeyValue.objects.update_or_create(key=key, defaults={'value': value})
        save_to_cache(key, value)
        
        return Response({'success': True, 'key': key, 'value': value}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class GetViewCashe(APIView):
    def get(self, request, key, *args, **kwargs):
        # Try to get the value from the cache first.
        value = get_from_cache(key)
        
        if value is None:
            # If not cached, retrieve from the database.
            value = get_from_db(key)
            if value is None:
                return JsonResponse({'error': 'Key not found.'}, status=404)
        
        return JsonResponse({'key': key, 'value': value}, status=200)

