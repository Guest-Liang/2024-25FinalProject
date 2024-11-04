# backend/api/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('decrypt/', DecryptView.as_view(), name='decrypt'),
    path('encrypt/', EncryptView.as_view(), name='encrypt'),
    path('echo/', EchoView.as_view(), name='echo'),
]
