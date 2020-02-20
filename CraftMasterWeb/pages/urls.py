from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('downloads', views.downloads, name="downloads"),
    path('team', views.team, name="team"),
    path('index', views.index, name="index"),
 ]
