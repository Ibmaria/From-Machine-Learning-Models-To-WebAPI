from django import forms


class MovieForm(forms.Form):
    title = forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Movie Title '}))
