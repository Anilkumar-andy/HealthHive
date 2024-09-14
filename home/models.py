from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags


# Create your models here.
class Carousel(models.Model):
    image=models.ImageField(upload_to='carousel/')
    title=RichTextField()
    description=RichTextField()
    def __str__(self) :
        return strip_tags(self.title)
