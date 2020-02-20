from django.urls import path
from . import views
urlpatterns = [
    path('emailSuccess',views.getEmail, name="email")
 ]
