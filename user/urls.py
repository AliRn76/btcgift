from django.urls import path
from user.views import OTPAPIView, AddressAPIView, LoginAPIView

urlpatterns = [
    path('otp/', OTPAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('address/', AddressAPIView.as_view()),
]
