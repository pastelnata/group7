from django import forms

class SupportForm(forms.Form):
    email = forms.EmailField(label='Your Email', required=True)
    subject = forms.CharField(label='Subject', max_length=100)
    content = forms.CharField(label='Message', widget=forms.Textarea)
