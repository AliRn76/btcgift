from rest_framework.generics import ListAPIView

from faq.models import FAQ
from faq.serializers import FAQSerializer


class FAQAPIView(ListAPIView):
    queryset = FAQ.active.all()
    serializer_class = FAQSerializer
