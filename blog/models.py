from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import User


class Blog(models.Model):
    def blog_covers_path(self, file_name):
        return f'blog/{file_name}'

    id = models.BigAutoField(db_column='ID', primary_key=True)
    title = models.CharField(db_column='Title', max_length=31)
    summary = models.CharField(db_column='Summary', max_length=63)
    text = models.TextField(db_column='Text')
    cover = models.ImageField(db_column='Cover', upload_to=blog_covers_path, blank=True, null=True)
    like_count = models.IntegerField(db_column='LikeCount', default=0)
    view_count = models.IntegerField(db_column='ViewCount', default=0)
    comment_count = models.IntegerField(db_column='CommentCount', default=0)
    date_updated = models.DateTimeField(db_column='DateUpdated', auto_now=True)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)

    class Meta:
        db_table = 'Blog'

    def like(self, user: User):
        self.like_count = F('like_count') + 1
        self.update(update_fields=['like_count'])
        like, _ = BlogLike.objects.get_or_create(user_id=user, blog_id=self.id)
        return like

    def view(self, user: User):
        self.like_count = F('view_count') + 1
        self.update(update_fields=['view_count'])
        view, _ = BlogView.objects.get_or_create(user_id=user, blog_id=self.id)
        return view


class BlogCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_approved=True).order_by('-id')


class BlogComment(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    is_approved = models.BooleanField(db_column='IsApproved', default=False)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    blog_id = models.ForeignKey(Blog, db_column='BlogID', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, db_column='UserID', on_delete=models.CASCADE)

    objects = models.Manager()
    approved = BlogCommentManager()

    class Meta:
        db_table = 'BlogComment'


@receiver(post_save, sender=BlogComment)
def increment_blog_comment_count(sender, instance=None, created=False, **kwargs):
    if created:
        instance.blog_id.comment_count = F('comment_count') + 1
        instance.blog_id.update(update_fields=['comment_count'])


class BlogLike(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    blog_id = models.ForeignKey(Blog, db_column='BlogID', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, db_column='UserID', on_delete=models.CASCADE)

    class Meta:
        db_table = 'BlogLike'


class BlogView(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    blog_id = models.ForeignKey(Blog, db_column='BlogID', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, db_column='UserID', on_delete=models.CASCADE)

    class Meta:
        db_table = 'BlogView'
