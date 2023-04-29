from rest_framework.response import Response
from rest_framework import generics, views, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from user.models import User, UserFollowing
from user.serializers import UserSerializer, UserFollowingSerializer


class UserRegistryView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserManageView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user


class LogoutView(views.APIView):
    """Logout view, get refresh_token argument and add refresh token to blacklist"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        email = self.request.query_params.get('email', None)
        if email:
            queryset = queryset.filter(email__icontains=email)

        return queryset

    @action(methods=['get'], detail=True, url_path='follow', url_name='follow',
            permission_classes=[IsAuthenticated], serializer_class=UserFollowingSerializer)
    def follow(self, request, pk=None):
        """Action for following on user"""
        data = {
            'following': self.get_object().id,
            'follower': self.request.user.id
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='unfollow', url_name='unfollow',
            permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        """Action for unfollowing on user"""
        try:
            follow = UserFollowing.objects.get(following=self.get_object(), follower=self.request.user)
        except UserFollowing.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
