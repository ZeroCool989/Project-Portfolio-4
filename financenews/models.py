from django.db import models
# Importing the correct User model
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Status choices for posts
STATUS = ((0, "Draft"), (1, "Published"))

# Post model representing a blog post


class Post(models.Model):
    # The title of the post
    title = models.CharField(max_length=200, unique=True)
    # URL-friendly version of the post's title
    slug = models.SlugField(max_length=200, unique=True)
    # ForeignKey linking the post to a user (author)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts")
    # Timestamp for when the post was last updated
    update_on = models.DateTimeField(auto_now=True)
    content = models.TextField()  # Main content/body of the post
    # Image associated with the post (using Cloudinary for cloud storage)
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)  # Short snippet/preview of the post
    # Timestamp for when the post was created
    created_on = models.DateTimeField(auto_now_add=True)
    # Adding the status field to the Post model
    status = models.IntegerField(choices=STATUS, default=0)
    # ManyToManyField to represent likes by users
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    # Metadata for the model, to order posts by creation date (most recent first)
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    # Returns the number of likes a post has
    def number_of_likes(self):
        return self.likes.count()

# Comment model representing comments on a post


class Comment(models.Model):
    # ForeignKey linking the comment to a specific post
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)  # Name of the commenter
    email = models.EmailField()  # Email of the commenter (not necessarily a user's email)
    body = models.TextField()  # Main content/body of the comment
    # Timestamp for when the comment was created
    created_on = models.DateTimeField(auto_now_add=True)
    # Flag to indicate if the comment has been approved
    approved = models.BooleanField(default=False)

    # Metadata for the model, to order comments by creation date (oldest first)
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
