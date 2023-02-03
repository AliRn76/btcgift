from django.urls import path
from card.views import CardCostAPIView, OrderAPIView, MyCardsAPIView, MyCardAPIView, RetrieveOrderAPIView

urlpatterns = [
    path('', OrderAPIView.as_view()),
    path('own/', MyCardsAPIView.as_view()),
    path('costs/', CardCostAPIView.as_view()),
    path('<str:id>/', RetrieveOrderAPIView.as_view()),
    path('own/<str:id>/', MyCardAPIView.as_view()),
]
