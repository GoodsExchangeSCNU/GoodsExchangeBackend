from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from ..views import userView

urlpatterns = [
    path('login',TokenObtainPairView.as_view(),name='login'),
    path('refresh',TokenRefreshView.as_view(),name='refresh'),
    path('register',userView.RegisterView.as_view(),name='register'),
    path("update",userView.UserView.as_view(),name='user api'),
    path("info",userView.UserView.as_view(),name='user api with search')
]