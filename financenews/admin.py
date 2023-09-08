from django.contrib import admin  # Admin module for customizing admin interface
# Importing Post model to register on admin site
from .models import Post, Comment
# Summernote provides a rich text editor for Django
from django_summernote.admin import SummernoteModelAdmin


# Registering Post model with admin site using Summernote for content editing
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    # These show up as columns in the admin list
    list_display = ('title', 'slug', 'status', 'created_on')

    # This lets us search posts using title and content
    search_fields = ['title', 'content']

    # Using the title to automatically generate a slug
    prepopulated_fields = {'slug': ('title',)}

    # Adding filters for status and date in admin
    list_filter = ('status', 'created_on')

    # Using Summernote editor for the content field
    summernote_fields = ('content')


# Registering Comment model with admin site
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    # Columns to show in the list view of comments in the admin panel
    list_display = ('name', 'body', 'post', 'created_on', 'approved')

    # Criteria available to filter the list of comments
    list_filter = ('approved', 'created_on')

    # Fields in which the admin can search for a specific comment
    search_fields = ('name', 'email', 'body')

    # List of available actions for admin.
    actions = ['approve_comments']

    # Mark selected comments as approved.
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
