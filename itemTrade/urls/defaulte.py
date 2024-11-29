from django.urls import path
from ..views import defaultView

urlpatterns = [
    path('recommend',defaultView.RecommandView.as_view()),
    path('search',defaultView.SearchView.as_view())
]
