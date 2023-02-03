from datetime import timedelta

from django.db import models
from django.db.models import F, Q
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from config.base_manager import BaseManager
from user.models import User


class Blog(models.Model):
    def blog_covers_path(self, file_name):
        return f'blog/{file_name}'

    id = models.BigAutoField(db_column='ID', primary_key=True)
    title = models.CharField(db_column='Title', max_length=31)
    summary = models.CharField(db_column='Summary', max_length=1023)
    content = models.TextField(db_column='Content')
    time_to_read = models.PositiveIntegerField(db_column='TimeToRead', default=0)
    cover = models.ImageField(db_column='Cover', upload_to=blog_covers_path)
    like_count = models.PositiveIntegerField(db_column='LikeCount', default=0)
    view_count = models.PositiveIntegerField(db_column='ViewCount', default=0)
    comment_count = models.PositiveIntegerField(db_column='CommentCount', default=0)
    date_updated = models.DateTimeField(db_column='DateUpdated', auto_now=True)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)

    objects = BaseManager()

    class Meta:
        db_table = 'Blog'

    def like(self, user: User):
        self.like_count = F('like_count') + 1
        self.save(update_fields=['like_count'])
        like, _ = BlogLike.objects.get_or_create(user_id=user, blog_id=self)
        return like

    def view(self, ip: str | None):
        """User can view a blog every 'x' timedelta"""
        x = timedelta(minutes=1)
        if ip is None or BlogView.objects.filter(ip=ip, date_created__gte=(timezone.now() - x)).first():
            return

        self.view_count = F('view_count') + 1
        self.save(update_fields=['view_count'])
        view = BlogView.objects.create(ip=ip, blog_id=self)
        return view

    def get_next_blog(self):
        blog = Blog.objects.filter(id__gt=self.id).first()
        if blog is None:  # self was the last blog
            blog = Blog.objects.first()
        return blog

    def get_prev_blog(self):
        blog = Blog.objects.filter(id__lt=self.id).last()
        if blog is None:  # self was the first blog
            blog = Blog.objects.last()
        return blog


class BlogCommentManager(models.Manager):
    def first_10(self, blog_id, user_id):
        # TODO: How should we index when we have AND and OR together
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_approved=True) | Q(user_id=user_id),
                blog_id=blog_id,
            )
            .order_by('is_approved', '-id')[:10]
        )

    def approved(self, blog_id, user_id):
        return super().get_queryset().filter(is_approved=True)


class BlogComment(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    is_approved = models.BooleanField(db_column='IsApproved', default=False)
    text = models.TextField(db_column='Text', max_length=255)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    blog_id = models.ForeignKey(Blog, db_column='BlogID', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, db_column='UserID', on_delete=models.CASCADE)

    objects = BlogCommentManager()

    class Meta:
        db_table = 'BlogComment'


@receiver(post_save, sender=BlogComment)
def increment_blog_comment_count(sender, instance=None, created=False, **kwargs):
    if created:
        instance.blog_id.comment_count = F('comment_count') + 1
        instance.blog_id.save(update_fields=['comment_count'])


class BlogLike(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    user_id = models.ForeignKey(User, db_column='UserID', on_delete=models.CASCADE)
    blog_id = models.ForeignKey(Blog, db_column='BlogID', on_delete=models.CASCADE)

    class Meta:
        db_table = 'BlogLike'


class BlogView(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    ip = models.GenericIPAddressField(db_column='IP')
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    blog_id = models.ForeignKey(Blog, db_column='BlogID', on_delete=models.CASCADE)

    class Meta:
        db_table = 'BlogView'
