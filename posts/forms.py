from django import forms
from .models import Post, PostImage, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write something...'
            })
        }


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['file']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']