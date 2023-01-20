from django.urls import path
from card.views import CardCostAPIView


urlpatterns = [
    path('costs/', CardCostAPIView.as_view())
]
