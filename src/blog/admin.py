from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'author', 'date_created', 'is_deleted']
    search_fields = ['title', 'subtitle', 'body']
    list_filter = ['author', 'date_created', 'is_deleted']
    date_hierarchy = 'date_created'
    readonly_fields = ['date_created']
