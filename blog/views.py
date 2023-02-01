from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from blog.models import Blog, BlogComment
from blog.serializers import BlogSerializer, RetrieveBlogSerializer, BlogLikeSerializer, BlogCommentSerializer
from config.paginations import NormalPagination


class BlogViewSet(ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    pagination_class = NormalPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveBlogSerializer
        return BlogSerializer


class BlogLikeAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogLikeSerializer


class BlogCommentsAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = NormalPagination
    serializer_class = BlogCommentSerializer

    def get_queryset(self):
        return BlogComment.objects.first_10(blog_id=self.kwargs['blog_id'], user_id=self.request.user.id)
