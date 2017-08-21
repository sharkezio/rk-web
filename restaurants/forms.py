from django import forms


class CommentForm(forms.Form):
    visitor = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=20, required=False,
                             label='E-mail')
    content = forms.CharField(max_length=200, widget=forms.Textarea())
