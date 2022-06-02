from dataclasses import field
from django import forms

from .models import Posts


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["post_image", "post_caption"]
