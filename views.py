from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import PostSerializer
from like.serializers import LikeSerializer
from .models import Posts
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from like.models import Like


class PostView(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'delete', 'retrieve']


    @action(method=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                like = Like.objects.get(post=post, author=user)
                like.delete()
                message = 'unliked'
            except Like.DoesNotExist:
                Like.objects.create(post=post, author=user)
                message = 'liked'
            return Response(message, status=201)