from django.db.models import Q
from rest_framework import viewsets, permissions, mixins

from post.serializer import PostSerializer, PostListSerializer, PostCreateSerializer
from post.models import Post
from user.models import User


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.select_related('author')
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ('retrieve', 'destroy'):
            queryset = queryset.filter(author=self.request.user)
        if self.action == 'list':
            queryset = queryset.filter(Q(author=self.request.user) |
                                       Q(author__in=User.objects.filter(followers__follower=self.request.user)))
        ids = self.request.query_params.get('id', None)
        if ids:
            ids = self._params_to_ints(ids)
            queryset = queryset.filter(author_id__in=ids)
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return PostListSerializer
        if self.action in ('create', 'update'):
            return PostCreateSerializer

        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
