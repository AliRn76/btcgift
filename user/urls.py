from django.urls import path
from user.views import OTPAPIView, AddressAPIView, LoginAPIView, ProfileAPIView

urlpatterns = [
    path('otp/', OTPAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('address/', AddressAPIView.as_view()),
]
