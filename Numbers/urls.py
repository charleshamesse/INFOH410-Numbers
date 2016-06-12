"""Numbers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.generic import TemplateView
# from django.contrib import admin
from app import views;
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    #url(r'^$', TemplateView.as_view(template_name="index.html"), name='index')
    url(r'^$', views.index, name='index'),
    url(r'^nn/train$', views.train, name='train'),
    url(r'^nn/recognize',views.recognize, name='recognize'),
    url(r'^save',views.saveNet,name='saveNet'),
    url(r'^load',views.loadNet,name='loadNet'),
    url(r'^nn/mnist',views.recognizeMNist,name='nist')
]