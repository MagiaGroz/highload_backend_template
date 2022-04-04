from django.urls import path, include

from .views import UserListCreateView, UserDetailView, EmailViewSet, UserViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("email", EmailViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    # gets all user profiles and create a new profile
    path("users", UserListCreateView.as_view(), name="all-profiles"),
    # retrieves profile details of the currently logged in user
    path("users/<int:pk>", UserDetailView.as_view(), name="profile"),
    path('', include(router.urls))
]
