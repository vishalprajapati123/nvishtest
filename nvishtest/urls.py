"""
URL configuration for nvishtest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from exercise1.views import *
from exercise2.views import *
from exercise3.views import *
from exercise4.views import *


urlpatterns = [
    path('admin/', admin.site.urls),

    path('ping', PingView.as_view(), name='ping'),

    path('authorize', AuthorizeView.as_view(), name='authorize'),
    path('generate-token', GenerateTokenView.as_view(), name='generate-token'),

    path('save', SaveView.as_view(), name='save'),
    path('get', GetValueView.as_view(), name='get_value'),
    path('delete', DeleteView.as_view(), name='delete'), 

    path('cashe/save', SaveViewCashe.as_view(), name='cashesave'),
    path('cashe/get/<str:key>', GetViewCashe.as_view(), name='casheget'),
]
