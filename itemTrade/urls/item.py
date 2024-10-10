from django.urls import path
from ..views import itemView

urlpatterns = [
    path('',itemView.ItemView.as_view(),name="crud item"),
    path('list',itemView.ItemListView.as_view(),name="get many item"),
    path('comment',itemView.CommentView.as_view(),name="post comments")
]