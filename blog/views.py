from rest_framework.viewsets import ModelViewSet
from blog.models import Blog
from blog.serializers import BlogSerializer
from config.paginations import NormalPagination


class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = NormalPagination
