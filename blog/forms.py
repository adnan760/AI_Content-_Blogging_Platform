from django import forms
from .models import PostModel, Comment


class PostModelForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 100%; height: 40px;'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 100%; height: 400px;'}))


    class Meta:
        model = PostModel
        fields = ('title', 'content')
        


class PostUpdateForm(forms.ModelForm):

    title = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 100%; height: 40px;'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 100%; height: 400px;'}))

    class Meta:
        model = PostModel
        fields = ('title', 'content')


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='', widget=forms.TextInput(attrs={'placeholder': 'Add comment here....','style': 'width: 100%; height: 40px; border: 1px solid #ccc;'}))

    class Meta:
        model = Comment
        fields = ('content',)