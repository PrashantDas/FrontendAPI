from django import forms


class EditNote(forms.Form):
    title = forms.CharField()
    matter = forms.CharField()