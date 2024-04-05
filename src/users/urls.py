from . import views
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('users/user/', views.UserCreateView.as_view(), name="signup"),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('', include(router.urls)),
    path('logout/', TokenBlacklistView.as_view(), name="token_blacklist"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]