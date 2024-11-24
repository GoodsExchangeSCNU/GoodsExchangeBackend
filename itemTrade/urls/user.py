from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from ..views import userView

urlpatterns = [
    path('login',TokenObtainPairView.as_view(),name='login'),
    path('refresh',TokenRefreshView.as_view(),name='refresh'),
    path('register',userView.RegisterView.as_view(),name='register'),
    path('password',userView.ModifyPasswordView.as_view(),name='modifyPassword'),
    path("update",userView.UserView.as_view(),name='user api'),
    path("info",userView.UserView.as_view(),name='user api with search'),
    path("info/<slug:username>",userView.UserView.as_view(),name="user api with search"),
    path("comment",userView.UserCommentView.as_view(),name="user trade comment"),
    path("record/buy",userView.BuyerRecordView.as_view(),name="buyerRecordApi"),
    path("record/sell",userView.SellerRecordView.as_view(),name="buyerRecordApi")
]
