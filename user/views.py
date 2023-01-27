from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config.settings import OTP_EXP
from user.messages import OPTSentSuccessfullyMessage
from user.models import Address
from user.serializers import ConfirmOTPSerializer, AddressSerializer


class AuthenticationAPIView(CreateAPIView):
    serializer_class = ConfirmOTPSerializer

    def get(self, request, *args, **kwargs):
        data = {'detail': OPTSentSuccessfullyMessage, 'otp_exp': OTP_EXP}
        return Response(data=data, status=status.HTTP_200_OK)


class AddressAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

