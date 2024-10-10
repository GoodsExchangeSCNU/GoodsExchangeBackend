from django.urls import path, include
from . import user,chat

urlpatterns = [
    path('user/',include(user.urlpatterns)),
    path('chat/',include(chat.urlpatterns))
]
