from django.urls import path, include

from .views import EmailViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("email", EmailViewSet)

urlpatterns = [
    path('', include(router.urls))
]
