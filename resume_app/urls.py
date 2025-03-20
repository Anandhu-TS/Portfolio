from django.urls import path
from . import views

urlpatterns = [
    path('', views.resume, name='resume'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
]