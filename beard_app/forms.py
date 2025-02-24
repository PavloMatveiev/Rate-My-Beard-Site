from django import forms
from .models import Post, Comment, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import HiddenInput
from django.forms.widgets import ClearableFileInput

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required field.")
    avatar = forms.ImageField(required=False, help_text="Select an avatar (optional).")

    class Meta:
        model = User
        fields = ("username", "email", "avatar", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Create a profile with an avatar if one is passed
            Profile.objects.create(user=user, avatar=self.cleaned_data.get("avatar"))
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'title', 'description']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': ClearableFileInput(attrs={'class': 'form-control'}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['rating', 'comment']
        widgets = {
            'rating': HiddenInput(),
        }

class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Enter password to confirm"
    )

