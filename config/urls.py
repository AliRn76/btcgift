from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('card/', include('card.urls')),
    # path('payment/', include('payment.urls')),
    # path('support/', include('support.urls')),
]
