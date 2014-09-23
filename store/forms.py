from django import forms


class CommentsForm(forms.Form):
    comments = forms.TextInput(attrs={'class': 'comments'})
