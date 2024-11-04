from crispy_forms.helper import FormHelper
from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory

from ForumApp.posts.mixins import DisableFieldsMixin
from ForumApp.posts.models import Post, Comment


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('approved', )

        error_messages = {
            'title': {
                'required': 'Please enter a title.',
                'max_length': f'The title must be under {Post.TITLE_MAX_LENGTH}.',
            },
            'author': {
                'required': 'Please enter an author.',
            },
        }

    def clean_author(self):
        author = self.cleaned_data.get('author')

        if not author[0].isupper():
            raise ValidationError('Author name should start with a capital letter!')

        return author

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and content and title in content:
            raise ValidationError('The title cannot be in the content.')

        return cleaned_data

    def save(self, commit=True):
        post = super().save(commit=False)

        post.title = post.title.capitalize()

        if commit:
            post.save()

        return post


class PostCreateForm(PostBaseForm):
    pass


class PostEditForm(PostBaseForm):
    pass


class PostDeleteForm(PostBaseForm, DisableFieldsMixin):
    disabled_fields = ('__all__',)


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        required=False,
        error_messages={
            'max_length': 'Please write something under 100 characters.',
        },
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for a post'
            }
        )
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'get'
    #     self.helper.form_class = 'form-inline'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']

        labels = {
            'author': '',
            'content': '',
        }

        error_messages = {
            'author': {
                'required': 'author is required',
            },
            'content': {
                'required': 'content is required',
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['author'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your name',
        })

        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Add a comment...',
        })


CommentFormSet = formset_factory(CommentForm, extra=2)
