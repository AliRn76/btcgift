from django.urls import path
from faq.views import FAQAPIView


urlpatterns = [
    path('', FAQAPIView.as_view()),
]
