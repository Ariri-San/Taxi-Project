from django.urls import path
from . import views


api_url = [
    path('check_admin/', views.CheckAdmin.as_view())
]

urlpatterns = api_url
