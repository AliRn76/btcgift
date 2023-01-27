from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from blog.models import Blog
from blog.serializers import BlogSerializer, RetrieveBlogSerializer, BlogLikeSerializer
from config.paginations import NormalPagination


class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.all()
    pagination_class = NormalPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveBlogSerializer
        else:
            return BlogSerializer


class BlogLikeAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogLikeSerializer
