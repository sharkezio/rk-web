from django import forms


class CommentForm(forms.Form):
    visitor = forms.CharField(max_length=20,
                              widget=forms.TextInput(
                                  attrs={'readonly': 'readonly',
                                         'style': 'background-color: #ffffb3'}))
    email = forms.EmailField(max_length=40, required=False,
                             label='E-mail',
                             widget=forms.EmailInput(attrs={'size': "35", }))
    content = forms.CharField(max_length=200, widget=forms.Textarea())
