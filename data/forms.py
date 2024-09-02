from .models import Video,Image,VideoReview,CustomPlans
from django import forms
from account.models import PlatformUser

class Video_form(forms.ModelForm):
    class Meta:
        model= Video
        exclude =['user']

class Image_form(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['user']


class VideoReview_form(forms.ModelForm):
    class Meta:
        model = VideoReview
        fields=['review']
        
class CustomPlans_form(forms.ModelForm):
    class Meta:
        model = CustomPlans
        fields = ['uploaded_for_user','week','plan_pdf','from_date','to_date']
        widgets = {
            'from_date':forms.DateInput(attrs={'type':'date'}),
            'to_date':forms.DateInput(attrs={'type':'date'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uploaded_for_user'].queryset=PlatformUser.objects.filter(subscription=True)
