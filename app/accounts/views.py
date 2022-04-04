from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, )
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, views, viewsets
from .models import User
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import UserSerializer
from rest_framework.response import Response
from djoser.serializers import ActivationSerializer
from rest_framework.decorators import action
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render


class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    token_generator = default_token_generator
    lookup_field = User._meta.pk.name

    def get_instance(self):
        return self.request.user

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
        return render(request, 'confirmation.html')
