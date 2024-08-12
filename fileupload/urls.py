from django.contrib import admin
from django.urls import path
from fileupload import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('summary/<int:file_id>/', views.summary_report, name='summary_report'),
]