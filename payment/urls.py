from django.urls import path
from payment.views import PaymentAPIView


urlpatterns = [
    path('verify/<int:transaction_id>/', PaymentAPIView.as_view()),
]
