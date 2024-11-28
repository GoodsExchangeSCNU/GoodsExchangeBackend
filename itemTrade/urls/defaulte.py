from django.urls import path
from ..views import defaultView

urlpatterns = [
    path('recommand',defaultView.RecommandView.as_view()),
    path('search',defaultView.SearchView.as_view())
]
