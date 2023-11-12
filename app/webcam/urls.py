from django.urls import path
from rest_framework.routers import SimpleRouter

from webcam import views

app_name = 'webcam'

urlpatterns = [
    path('all/', views.WebcamList.as_view(), name='webcam_list'),
]
