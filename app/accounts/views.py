from django.contrib.auth import get_user_model
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, )
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, views, viewsets
from .models import UserProfile
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from djoser.serializers import ActivationSerializer
from rest_framework.decorators import action
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class UserProfileListCreateView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    token_generator = default_token_generator
    lookup_field = User._meta.pk.name

    def get_instance(self):
        return self.request.user.profile

    def retrieve(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serialized = self.serializer_class(user_profile)
        return Response(serialized.data)

    @action(["get", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)


class EmailViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    token_generator = default_token_generator

    def get_serializer_class(self):
        if self.action == "activation":
            return ActivationSerializer

    @action(["get"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

