from django.urls import path
from .views import UserViewSet, AuthenticatedUserView, ContactView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    # TokenVerifyView
)
from .views import LogInView


app_name = 'users'
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls
urlpatterns += [
    path('auth/', AuthenticatedUserView.as_view(), name='authenticated_user'),
    path('login/', LogInView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('contact/', ContactView.as_view(), name='authenticated_user'),
]
