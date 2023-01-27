from rest_framework import serializers
from blog.models import Blog, BlogComment, BlogLike
from config.utils import client_ip


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = '__all__'


class RetrieveBlogSerializer(serializers.ModelSerializer):
    comments = BlogCommentSerializer(source='blogcomment_set', many=True)
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [field.name for field in model._meta.fields]
        fields.extend(['comments', 'liked'])

    def get_liked(self, blog):
        user = self.context['request'].user
        if user.is_authenticated and BlogLike.objects.filter(user_id=user.id, blog_id=blog.id).first():
            return True
        return False

    def to_representation(self, instance):
        instance.view_count += 1  # For Perfection :)
        response = super().to_representation(instance)
        instance.view(client_ip(self.context))
        return response


class BlogLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogLike
        exclude = ['user_id']

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)
