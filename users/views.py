from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import UserSerializer
from .utils import get_tokens_for_user


class RegisterView(CreateAPIView):

    model = get_user_model()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_tokens = get_tokens_for_user(user)
        headers = self.get_success_headers(serializer.data)
        return Response(user_tokens, status=status.HTTP_201_CREATED, headers=headers)
