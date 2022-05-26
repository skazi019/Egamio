from django.shortcuts import render
from django.db.models import Count

from .models import Profile, Posts, Followers, Comments, Replies


def index(request):
    all_posts = (
        Posts.objects.all()
        .order_by("-post_date")
        .annotate(
            number_of_comments=Count("post_comment"),
            # to get the number of comments on individual post
        )
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
    profile = Profile.objects.get(
        user=request.user
    )  # returns profile object for the current user
    current_user = (
        profile.user
    )  # getting the user details from the auth user model linked to profile model
    users_liked_post = [
        user.user for user in post.post_likes.all()
    ]  # post.post_likes.all() gives list of profiles of all users who have liked the post

    if current_user in users_liked_post:
        post.post_likes.remove(profile)
        user_action = "removed"
    else:
        post.post_likes.add(profile)
        user_action = "added"
    return render(
        request=request,
        template_name="update_likes.html",
        context={
            "post": post,
            "user_action": user_action,
        },
    )


def get_post(request, pk):
    post = Posts.objects.get(id=pk)
