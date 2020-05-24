from django import forms
from taggit.forms import TagField
from django.utils import timezone


from .models import Question, Answer, Profile


class add_post(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['author_id']

        title = forms.CharField(label='Question title', widget=forms.TextInput(attrs={'class': 'form-control', 'size': 64}))
        text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'size': 64}), label='Question text')
        tags = TagField( label='Tags', widget=forms.TextInput(attrs={'class': 'form-control'}))
        create_date = timezone.now()
        required_css_class = "fields"


class add_answer(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ['question', 'author_id', 'create_date']

        text = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea control-check', 'size': 64}), label='Answer text')


class add_register(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'img']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'size': 64}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'size': 64}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'size': 64}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'size': 64}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'size': 64}),
            'img': forms.FileInput(attrs={'upload_to': 'media'}).attrs.update({'required': False})
        }


class setting_profile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'first_name', 'last_name', 'img']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'size': 64}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'size': 64}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': False}),
            'img': forms.FileInput(attrs={'upload_to': 'media'}).attrs.update({'required': False})
        }
