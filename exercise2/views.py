from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from .authentication import *

User = get_user_model()

class AuthorizeView(APIView):
    """
    This view checks if the request is authenticated using custom pre-shared key token authentication.
    """
    authentication_classes = [PreSharedKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        return Response({
            "detail": "User is authenticated.",
            "user": request.user.username  # Example of including user-specific data
        }, status=status.HTTP_200_OK)


class GenerateTokenView(APIView):
    """
    This view generates a token for a superuser upon request.
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        if user.is_superuser:
            token, created = Token.objects.get_or_create(user=user)
            status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response({'token': token.key}, status=status_code)
        else:
            return Response({'detail': 'User is not a superuser.'}, status=status.HTTP_403_FORBIDDEN)
