from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
path('movie/', views.index, name='movie'),
path('spam/', views.spam, name='spam'),
path('predict_spam/', views.predict_spam, name='predict_spam'),
path('predict_movie/', views.predict_movie, name='predict_movie'),
   
]