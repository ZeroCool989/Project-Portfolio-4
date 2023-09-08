from django.contrib import admin  # Admin module for customizing admin interface
from .models import Post  # Importing Post model to register on admin site
# Summernote provides a rich text editor for Django
from django_summernote.admin import SummernoteModelAdmin

# Registering Post model with admin site using Summernote for content editing


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    # Using Summernote editor for the content field
    summernote_fields = ('content')
