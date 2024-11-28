from django.urls import path, include

from . import user,item,trade,chat,defaulte

urlpatterns = [
    path('user/',include(user.urlpatterns)),
    path('item/',include(item.urlpatterns)),
    path('trade/',include(trade.urlpatterns)),
    path('chat/',include(chat.urlpatterns)),
    path('',include(defaulte.urlpatterns))
]
