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
