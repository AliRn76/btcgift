from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from config.utils import validate_phone_number
from user.authentication import JWTAuthentication
from user.models import User, Address


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, phone_number):
        if (_phone_number := validate_phone_number(phone_number)) is None:
            raise ValidationError('phone_number not valid')
        return _phone_number


class ConfirmOTPSerializer(PhoneNumberSerializer):
    otp = serializers.CharField()

    def validate_otp(self, otp):
        if otp != '1111':
            raise ValidationError('otp Is not valid')
        return otp

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(phone_number=validated_data['phone_number'])
        user.update_last_login()
        return user

    def to_representation(self, instance):
        token = JWTAuthentication.encode_jwt_token(instance)
        data = UserProfileSerializer(instance).data
        return token | data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_banned']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['user_id', 'is_deleted', 'is_tehran']

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user
        validated_data['is_tehran'] = True  # TODO: Neshan API
        return super().create(validated_data)
