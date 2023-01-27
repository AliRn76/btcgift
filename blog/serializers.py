from rest_framework import serializers
from blog.models import Blog, BlogComment, BlogLike
from config.utils import client_ip
from user.messages import SubmittedSuccessfullyMessage


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        exclude = ['user_id', 'blog_id', 'is_approved']

    def create(self, validated_data):
        blog = Blog.objects.get_or_raise(id=self.context['view'].kwargs['blog_id'])
        validated_data['blog_id'] = blog
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        if self.context['request'].method == 'POST':
            return {'detail': SubmittedSuccessfullyMessage}
        return super().to_representation(instance)


class RetrieveBlogSerializer(serializers.ModelSerializer):
    comments = BlogCommentSerializer(source='blogcomment_set', many=True)
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    def get_comments(self, blog):
        queryset = BlogComment.approved.filter(blog_id=blog.id)[:10]
        return BlogCommentSerializer(queryset, many=True)

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

    def to_representation(self, instance):
        return {'detail': SubmittedSuccessfullyMessage}