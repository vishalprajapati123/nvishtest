from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _

class PreSharedKeyAuthentication(TokenAuthentication):
    """
    Custom Token Authentication that accepts a Bearer token.
    """

    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        # Since we're using the same Token model, we call the super method
        # which will handle fetching the token for us.
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (token.user, token)