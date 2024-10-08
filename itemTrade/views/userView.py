from rest_framework import status,serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from ..serializers.userSerializers import UserSerializer,RegisterSerializer,RecordSerializer
from django.contrib.auth.models import User

from ..models import *

class RegisterView(APIView):
    """注册视图"""

    authentication_classes = []
    permission_classes = []

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'code':'0',
                'message':'注册成功'
            },status=status.HTTP_200_OK)

class UserView(APIView):
    """用户相关操作视图"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(sef,request,username=None):
        if not username:
            user = request.user
            serializer = UserSerializer(user)
            return Response({
                'code':0,
                'message':"获取成功",
                'data':serializer.data
            })
        else:
            try:
                user = User.objects.get(username=username)
                serializer = UserSerializer(user)
                return Response({
                    'code':0,
                    'message':"获取成功",
                    'data':serializer.data
                })
            except User.DoesNotExist:
                return Response({
                    'code':1,
                    'message':"用户不存在"
                })
            
    def put(self,requets):
        """修改用户信息"""
        user = requets.user
        serializer = UserSerializer(user, data=requets.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'code':0,
                'message':'修改成功'
            })

class BuyerRecordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = RecordSerializer

    def get(self,request):
        user = request.user
        recode = user.buy_trade
        serializer = self.serializer_class(recode,many=True)

        return Response({
            'code':0,
            'message':"获取成功",
            'data':serializer.data
        })


class SellerRecordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = RecordSerializer

    def get(self, request):
        user = request.user
        recode = user.sell_trade
        serializer = self.serializer_class(recode, many=True)

        return Response({
            'code': 0,
            'message': "获取成功",
            'data': serializer.data
        })
