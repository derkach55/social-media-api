from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from user.views import UserRegistryView, UserManageView, LogoutView, UserViewSet, FollowersListView, FollowingListView

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistryView.as_view(), name='register'),
    path('profile/', UserManageView.as_view(), name='profile'),
    path('profile/logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('followers/', FollowersListView.as_view(), name='followers'),
    path('followings/', FollowingListView.as_view(), name='followings')
]
app_name = 'user'
