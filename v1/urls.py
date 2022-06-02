from django.urls import path

from .views import (
    index,
    handle_like,
    get_users_liked_list,
    remove_users_liked_list,
    get_comments_modal,
    remove_comments_modal,
    add_comment_to_post,
    add_post,
    remove_post_modal,
)

urlpatterns = [
    path("add_post/", add_post, name="add_post"),
    path("remove_post_modal/", remove_post_modal, name="remove_post_modal"),
    path("handle_like/<int:pk>/", handle_like, name="handle_like"),
    path(
        "get_users_liked_list/<int:pk>/",
        get_users_liked_list,
        name="get_users_liked_list",
    ),
    path(
        "remove_users_liked_list/<int:pk>/",
        remove_users_liked_list,
        name="remove_users_liked_list",
    ),
    path(
        "add_comment_to_post/<int:pk>/",
        add_comment_to_post,
        name="add_comment_to_post",
    ),
    path(
        "remove_comments_modal/<int:pk>/",
        remove_comments_modal,
        name="remove_comments_modal",
    ),
    path(
        "get_comments_modal/<int:pk>/",
        get_comments_modal,
        name="get_comments_modal",
    ),
    path("", index, name="home"),
]
