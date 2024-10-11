from django.urls import path
from ..views import tradeView

urlpatterns = [
    path('update',tradeView.TradeView.as_view(),name="trade ru"),
    path('new',tradeView.TradeView.as_view(),name="trade c"),
    path('comment',tradeView.CommentView.as_view(),name="comment create"),
    path('roomlist',tradeView.RoomListView.as_view(),name="get room list")
]