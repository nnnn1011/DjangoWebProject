"""
Definition of urls for DjangoWebProject2.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
import pandas as pd
import mysql.connector
from mysql.connector import Error
import re
import pymysql

#Update and Delete page
def UD_DB(request):
    return render(request, 'insert_and_delete.html')


urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload, name='upload'),
    path('update_EDL', views.update_EDL, name='update_EDL'),
    path('insert_and_delete/', views.insert_and_delete, name='insert_and_delete'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
