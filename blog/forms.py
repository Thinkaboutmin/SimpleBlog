from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Post, Comment


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        """Custom constructor. Used to modify a few attributes from the form"""

        # Add the class attribute to use boostrap forms.
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"

class SigninForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        """Custom constructor. Used to modify a few attributes from the form"""

        # Add the class attribute to use boostrap forms.
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            })
        }
        labels = {
            "content": "Comment on this post"
        }