from django.urls import path, include
from . import user

urlpatterns = [
    path('user/',include(user.urlpatterns))
]