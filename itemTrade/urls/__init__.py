from django.urls import path, include
from . import user,item

urlpatterns = [
    path('user/',include(user.urlpatterns)),
    path('item/',include(item.urlpatterns))
]