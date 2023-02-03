from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import generate_otp
from config.messages import ProfileUpdatedMessage
from user.authentication import JWTAuthentication
from user.models import Address
from user.serializers import LoginSerializer, AddressSerializer, OTPSerializer, UserProfileSerializer


class OTPAPIView(CreateAPIView):
    serializer_class = OTPSerializer

    def perform_create(self, serializer):
        phone_number = serializer.validated_data['phone_number']
        otp = generate_otp()
        # REDIS.set(phone_number, otp, ex=OTP_EXP)
        # send_otp_sms(phone_number, otp)


class LoginAPIView(CreateAPIView):
    serializer_class = LoginSerializer


class RefreshTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        tokens = JWTAuthentication.encode_jwt_token(self.request.user)
        return Response(data=tokens, status=status.HTTP_202_ACCEPTED)


class ProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return {'detail': ProfileUpdatedMessage}


class AddressAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

