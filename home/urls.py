from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage,name='home_page'),
    path('links',views.important_links,name='important_links')
]
