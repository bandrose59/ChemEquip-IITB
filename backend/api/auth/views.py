from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *
from .jwt_auth import create_token

@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if User.objects.filter(username=username).exists():
        return Response({"message": "User exists"}, status=400)

    user = User.objects.create_user(username=username, password=password)

    return Response({"message": "Registered successfully"})

@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = User.objects.filter(username=username).first()

    if user is None or not user.check_password(password):
        return Response({"message": "Invalid credentials"}, status=400)

    token = create_token(user)

    return Response({"token": token})
