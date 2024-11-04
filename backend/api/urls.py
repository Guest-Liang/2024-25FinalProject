# backend/api/urls.py
from django.urls import path
from .views import DecryptView, EchoView

urlpatterns = [
    path('decrypt/', DecryptView.as_view(), name='decrypt'),
    path('echo/', EchoView.as_view(), name='echo'),
]
