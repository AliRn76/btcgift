from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from config.paginations import NormalPagination
from support.models import Support
from support.serializers import CreateSupportSerializer, SupportSerializer, SupportMessageSerializer


class SupportAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = NormalPagination

    def get_queryset(self):
        return Support.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateSupportSerializer
        return SupportSerializer


class SupportDetailAPIView(RetrieveAPIView, CreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Support.objects.get_or_raise(user_id=self.request.user.id, id=self.kwargs['id'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['support_id'] = self.kwargs['id']
        return context

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SupportMessageSerializer
        return SupportSerializer
