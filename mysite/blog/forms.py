from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'photo']  # Include photo field
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter post content'}),
        }
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
            'photo': 'Upload Photo',
        }

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:  # Assign the logged-in user as the author
            post.author = user
        if commit:
            post.save()
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your comment'}),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter rating (0.0 - 5.0)', 
                'min': 0, 
                'max': 5, 
                'step': 0.1
            }),
        }
        labels = {
            'content': 'Comment',
            'rating': 'Rating (Optional)',
        }

    def save(self, commit=True, user=None, post=None):
        comment = super().save(commit=False)
        if user:  # Assign the logged-in user as the author
            comment.author = user
        if post:  # Assign the post to which the comment belongs
            comment.post = post
        if commit:
            comment.save()
        return comment
