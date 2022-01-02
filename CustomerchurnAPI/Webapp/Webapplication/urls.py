from .import views
from django.urls import path

urlpatterns = [

path('', views.index_churn, name='churn'),
path('predict_churn/', views.predict_churn, name='predict_churn'),





]