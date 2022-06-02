from re import template
from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from .models import Profile, Posts, Followers, Comments, Replies
from .forms import PostForm


@login_required
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
    user_profile = Profile.objects.get(user=request.user)
    return render(
        request=request,
        template_name="home.html",
        context={
            "all_posts": all_posts,
            "comments": comments,
            "user_profile": user_profile,
        },
    )


@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()

        return render(
            request=request, template_name="modals/post_added.html", context={}
        )

    form = PostForm()

    return render(
        request=request,
        template_name="modals/add_post.html",
        context={
            "post_form": form,
        },
    )


@login_required
def remove_post_modal(request):
    return render(
        request=request, template_name="partials/remove_post_modal.html", context={}
    )


@login_required
def handle_like(request, pk):
    post = Posts.objects.get(id=pk)
    profile = Profile.objects.get(
        user=request.user
    )  # returns profile object for the current user
    current_user = (
        profile.user
    )  # getting the user details from the auth user model linked to profile model by one to one relation
    users_liked_post = [
        user.user for user in post.post_likes.all()
    ]  # post.post_likes.all() gives list of profiles of all users who have liked the post hence extracting the user objects from the one to one linked auth user model

    if current_user in users_liked_post:
        post.post_likes.remove(profile)
        user_action = "removed"
    else:
        post.post_likes.add(profile)
        user_action = "added"
    return render(
        request=request,
        template_name="partials/update_likes.html",
        context={
            "post": post,
            "user_action": user_action,
        },
    )


@login_required
def get_users_liked_list(request, pk):
    post = Posts.objects.get(id=pk)
    users = [user.user for user in post.post_likes.all()]
    return render(
        request=request,
        template_name="modals/modal_likes_list.html",
        context={
            "users": users,
            "post": post,
        },
    )


@login_required
def remove_users_liked_list(request, pk):
    post = Posts.objects.get(id=pk)
    return render(
        request=request,
        template_name="partials/update_users_liked_list.html",
        context={"post": post},
    )


@login_required
def get_comments_modal(request, pk):
    comments = Comments.objects.filter(post_id=pk)
    post = Posts.objects.get(id=pk)
    return render(
        request=request,
        template_name="modals/modal_comments.html",
        context={
            "comments": comments,
            "post": post,
        },
    )


@login_required
def remove_comments_modal(request, pk):
    comments = Comments.objects.filter(post_id=pk)
    post = Posts.objects.get(id=pk)
    return render(
        request=request,
        template_name="partials/remove_comments_modal.html",
        context={
            "post": post,
        },
    )


@login_required
def add_comment_to_post(request, pk):
    if request.method == "POST":
        user = request.user
        user_profile = Profile.objects.get(user=user)
        post = Posts.objects.get(pk=pk)
        user_comment = request.POST.get("user-comment")
        comment = Comments(user_id=user_profile, post_id=post, comment=user_comment)
        comment.save()
        all_comments = Comments.objects.filter(post_id=pk)
        return render(
            request=request,
            template_name="partials/add_comment_to_post.html",
            context={"comment": comment},
        )
