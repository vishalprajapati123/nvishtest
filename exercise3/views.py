from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import KeyValue

class SaveView(APIView):
    """
    This view allows posting a key-value pair to be saved to the database.
    """
    def post(self, request):
        key = request.data.get('key')  # Using request.data to handle form or json data
        value = request.data.get('value')

        if not key or not value:
            return Response({'error': 'Key and value are required.'}, status=status.HTTP_400_BAD_REQUEST)

        KeyValue.objects.update_or_create(key=key, defaults={'value': value})
        return Response({'key': key, 'value': value}, status=status.HTTP_201_CREATED)



class GetValueView(APIView):
    """
    This view returns the value for a given key from the database.
    """
    def get(self, request, *args, **kwargs):
        key = request.query_params.get('key')
        
        if not key:
            return Response({'error': 'Key is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            kv_pair = KeyValue.objects.get(key=key)
            return Response({'key': key, 'value': kv_pair.value}, status=status.HTTP_200_OK)
        except KeyValue.DoesNotExist:
            return Response({'error': 'Key not found.'}, status=status.HTTP_404_NOT_FOUND)


class DeleteView(APIView):
    """
    This view allows deleting a key-value pair from the database.
    """
    def delete(self, request):
        key = request.query_params.get('key')

        if not key:
            return Response({'error': 'Key is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            kv_pair = KeyValue.objects.get(key=key)
            kv_pair.delete()
            return Response({'message': 'Key-value pair deleted successfully.'}, status=status.HTTP_200_OK)
        except KeyValue.DoesNotExist:
            return Response({'error': 'Key not found.'}, status=status.HTTP_404_NOT_FOUND)