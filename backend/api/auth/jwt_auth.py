import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

SECRET = settings.SECRET_KEY

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")

        if not token:
            return None
        
        try:
            token = token.replace("Bearer ", "")
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            user = User.objects.get(id=payload["id"])
            return (user, None)
        except Exception:
            raise AuthenticationFailed("Invalid or expired token")

def create_token(user):
    payload = {
        "id": user.id,
        "exp": datetime.utcnow() + timedelta(days=3),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")
