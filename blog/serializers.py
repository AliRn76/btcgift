from rest_framework import serializers
from blog.models import Blog, BlogComment, BlogLike
from config.utils import client_ip
from config.messages import SubmittedSuccessfullyMessage
from user.serializers import MinUserProfileSerializer


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ['content']


class BlogMinimumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'time_to_read', 'cover']


class BlogCommentSerializer(serializers.ModelSerializer):
    user = MinUserProfileSerializer(source='user_id', read_only=True)

    class Meta:
        model = BlogComment
        exclude = ['user_id', 'blog_id']

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
    comments = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    next_blog = BlogMinimumSerializer(source='get_next_blog')
    prev_blog = BlogMinimumSerializer(source='get_prev_blog')

    class Meta:
        model = Blog
        fields = '__all__'

    def get_liked(self, blog):
        user = self.context['request'].user
        if user.is_authenticated and BlogLike.objects.filter(user_id=user.id, blog_id=blog.id).first():
            return True
        return False

    def get_comments(self, blog):
        queryset = BlogComment.objects.first_10(blog_id=blog.id, user_id=self.context['request'].user.id)
        return BlogCommentSerializer(queryset, many=True, context=self.context).data

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
