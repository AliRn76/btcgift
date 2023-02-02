from rest_framework import serializers
from config.messages import SubmittedSuccessfullyMessage
from support.models import Support, SupportMessages


class CreateSupportSerializer(serializers.ModelSerializer):
    message = serializers.CharField(max_length=1023, required=True)
    file = serializers.FileField(required=False)

    class Meta:
        model = Support
        fields = ['subject', 'message', 'file']

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user
        support = Support.objects.create(subject=validated_data['subject'], user_id=self.context['request'].user)
        SupportMessages.objects.create(
            message=validated_data['message'],
            file=validated_data['file'],
            is_answer=False,
            support_id=support
        )
        return support

    def to_representation(self, instance):
        return {'detail': SubmittedSuccessfullyMessage}


class SupportMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportMessages
        fields = ['id', 'is_answer', 'message', 'file', 'date_created']
        read_only_fields = ['is_answer']

    def create(self, validated_data):
        support = Support.objects.get_or_raise(id=self.context['support_id'])
        validated_data['support_id'] = support
        return super().create(validated_data)

    def to_representation(self, instance):
        if self.context['request'].method == 'POST':
            return {'detail': SubmittedSuccessfullyMessage}
        else:
            return super().to_representation(instance)


class SupportSerializer(serializers.ModelSerializer):
    messages = SupportMessageSerializer(source='supportmessages_set', many=True)

    class Meta:
        model = Support
        fields = ['id', 'subject', 'date_created', 'messages']
