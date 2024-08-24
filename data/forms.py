from .models import Video,Image
from django import forms

class Video_form(forms.ModelForm):
    class Meta:
        model= Video
        exclude =['user']

class Image_form(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['user']


