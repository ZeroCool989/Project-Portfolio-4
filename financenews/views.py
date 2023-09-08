from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post
from .forms import CommentForm
from django.http import HttpResponseForbidden


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )


class PostDetail(View):

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        # Initialize form with POST data
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            # Form is valid, save the comment and associated data
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user  # Assuming the user is authenticated
            new_comment.name = comment_form.cleaned_data['name']
            new_comment.email = comment_form.cleaned_data['email']
            new_comment.save()
        else:
            return HttpResponseForbidden("Invalid comment data")

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )
