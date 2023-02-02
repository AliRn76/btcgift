from django.urls import path
from support.views import SupportAPIView, SupportDetailAPIView

urlpatterns = [
    path('', SupportAPIView.as_view()),
    path('<int:id>/', SupportDetailAPIView.as_view()),

]
