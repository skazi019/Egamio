from django.urls import path

from .views import index, handle_like, get_post

urlpatterns = [
    path("handle_like/<int:pk>/", handle_like, name="handle_like"),
    path("get_post/<int:pk>/", get_post, name="get_post"),
    path("", index, name="home"),
]
