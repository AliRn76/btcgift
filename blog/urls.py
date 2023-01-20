from rest_framework import routers
from blog.views import BlogViewSet


router = routers.DefaultRouter()
router.register(r'', BlogViewSet)

urlpatterns = router.urls
