from django.db import models
from django.contrib.auth.models import User

from sorl.thumbnail import ImageField


class Profile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="auth_user"
    )
    bio = models.CharField(max_length=700)
    profile_pic = ImageField(
        upload_to="profilepictures",
        help_text="Image dimensions 96x96",
    )

    def display_username(self):
        return self.user.username

    display_username.short_description = "username"

    def __str__(self) -> str:
        return f"{self.user.username}"


class Followers(models.Model):
    class Meta:
        verbose_name = "Follower"
        verbose_name_plural = "Followers"

    user_id = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="%(class)s_user_id"
    )
    follower_id = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="%(class)s_follower_id",
        blank=False,
        null=True,
    )

    def __str__(self) -> str:
        return f"User: {self.user_id} | Follower: {self.follower_id}"


class Posts(models.Model):
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="post_author"
    )
    post_image = models.ImageField(upload_to="posts")
    post_date = models.DateField(auto_now_add=True)
    post_likes = models.ManyToManyField(Profile, related_name="post_like", blank=True)
    post_caption = models.CharField(max_length=700)
    post_date = models.DateField(auto_now_add=True)

    # Getting the number of likes for each post
    @property
    def number_of_likes(self):
        return self.post_likes.count()

    # Below list created to color the like button
    # This list gets all the usernames of the users who have liked the post
    # Using this for coloring the like button: if user is present in this list
    # then make the like button red else empty
    @property
    def users_who_liked(self):
        return [profile.user for profile in self.post_likes.all()]

    @property
    def get_post_image(self):
        if self.post_image and hasattr(self.post_image, "url"):
            return self.post_image.url

    def __str__(self) -> str:
        return f"{self.pk}"


class Comments(models.Model):
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    post_id = models.ForeignKey(
        Posts, on_delete=models.CASCADE, related_name="post_comment"
    )
    user_id = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="%(class)s_user_id"
    )
    comment = models.TextField(blank=False)

    def __str__(self) -> str:
        return f"{self.pk}"


class Replies(models.Model):
    class Meta:
        verbose_name = "Reply"
        verbose_name_plural = "Replies"

    user_id = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="%(class)s_user_id"
    )
    comment_id = models.ForeignKey(
        Comments, on_delete=models.CASCADE, related_name="%(class)s_comment_id"
    )
    reply = models.TextField(blank=False, null=True)

    def __str__(self) -> str:
        return f"{self.pk}"
