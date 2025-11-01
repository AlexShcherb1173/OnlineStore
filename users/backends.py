from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailAuthBackend(ModelBackend):
    """Аутентификация по email вместо username. На всякий случай"""

    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        login = (email or username or "").lower()
        if not login:
            return None
        try:
            user = User.objects.get(email__iexact=login)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
