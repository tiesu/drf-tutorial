from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import Post
from .permissions import IsOwner
from .serializers import PostSerializer


class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = []

        return super().get_permissions()


class PostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        self.permission_classes = [IsOwner]
        return super().get_permissions()