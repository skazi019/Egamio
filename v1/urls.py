from django.urls import path

from .views import index, handle_like, get_users_liked_list, remove_users_liked_list

urlpatterns = [
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
    path("", index, name="home"),
]
