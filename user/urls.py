from django.urls import path
from user.views import AuthenticationAPIView, AddressAPIView

urlpatterns = [
    path('authentication/', AuthenticationAPIView.as_view()),
    path('address/', AddressAPIView.as_view()),
]
