from django.contrib import admin

from .models import Profile, Followers, Posts, Comments, Replies


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", "display_username")


@admin.register(Followers)
class FollowersAdmin(admin.ModelAdmin):
    list_display = ("pk", "user_id", "follower_id")


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "post_date", "get_post_image", "number_of_likes")


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("pk", "post_id", "user_id", "comment")


@admin.register(Replies)
class RepliesAdmin(admin.ModelAdmin):
    list_display = ("pk", "comment_id", "user_id", "reply")
