from django.urls import path
from rest_framework import routers
from blog.views import BlogViewSet, BlogLikeAPIView

router = routers.DefaultRouter()
router.register(r'', BlogViewSet)

urlpatterns = [
    path('like/', BlogLikeAPIView.as_view())
]

urlpatterns += router.urls
