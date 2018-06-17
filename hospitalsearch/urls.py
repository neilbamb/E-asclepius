from django.views.generic.base import TemplateView, RedirectView
from . import models, views
from django.urls import path,include
from django.conf.urls import url
#from hospitalsearch.views import HomeView
from django.db.models import Q

app_name = 'hospitalsearch'

urlpatterns = [
    #path("",RedirectView.as_view(url="find"),name="find"),
    #path("find",views.find1,name="find"),
    path('find', views.search, name='find'),
    #url(r'^$', HomeView.as_view(), name='find'),
    #path("find", views.find,name="find"),
]
