from django.shortcuts import render
from django.db.models import Count

from .models import Profile, Posts, Followers, Comments, Replies


def index(request):
    all_posts = (
        Posts.objects.all()
        .order_by("-post_date")
        .annotate(
            number_of_comments=Count("post_comment")
        )  # to get the number of comments on 1 post
    )
    comments = Comments.objects.all()
    return render(
        request=request,
        template_name="home.html",
        context={
            "all_posts": all_posts,
            "comments": comments,
        },
    )


def handle_like(request, pk):
    post = Posts.objects.get(id=pk)
    user = Profile.objects.get(id=request.user.pk)
    users_liked_post = [user for user in post.post_likes.all()]
    comments = post.post_comment.all()
    if user in users_liked_post:
        post.post_likes.remove(user)
    else:
        post.post_likes.add(user)
    return render(
        request=request,
        template_name="likes.html",
        context={"post": post},
    )


def get_post(request, pk):
    post = Posts.objects.get(id=pk)
