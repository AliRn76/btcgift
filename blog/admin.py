from django.contrib import admin
from blog.models import Blog, BlogComment, BlogLike, BlogView


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'summary', 'date_updated', 'date_created')
    search_fields = ('id', 'title', 'summary', 'text')
    readonly_fields = ('like_count', 'view_count', 'comment_count')

    ordering = ('-id',)


class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_approved', 'text', 'date_created')
    search_fields = ('id', 'text')

    ordering = ('-id',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
admin.site.register(BlogLike)
admin.site.register(BlogView)
