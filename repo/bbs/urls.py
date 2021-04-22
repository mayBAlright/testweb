from django.urls import path
from . import views

app_name = 'bbs'
urlpatterns = [
    path('',views.home), 
    path('register/',views.register), 
    path('login/', views.login),
    path('logout/', views.logout),
]