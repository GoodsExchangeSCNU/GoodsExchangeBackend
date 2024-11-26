from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.db.models import Func, FloatField
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers.itemSerializers import ItemSerializer,ItemCommentSerializer
from ..models import Item
from ..utils.errors import ValidationError

class ItemView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializers_class = ItemSerializer

    @swagger_auto_schema(
        operation_summary="item upload interface",
        request_body=ItemSerializer,
        responses={
            200: openapi.Response(description="base responses")
        }
    )
    def post(self,request):
        user = request.user
        data = request.data
        images = data.getlist('img')

        new_data = {
            'name':data.get('name'),
            'description':data.get('description'),
            'count':data.get('count'),
            'price':data.get('price'),
            'owner':user.id,
            'img':[{"image":image} for image in images]
        }

        serializer = self.serializers_class(data=new_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'code':0,
                'message':"添加成功",
                'data':serializer.data
            })

    @swagger_auto_schema(
        operation_summary="get the detail message of item",
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                description="the id of the item",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: ItemSerializer
        }
    )
    def get(self,request):
        id = request.GET.get('id')
        if not id:
            return Response({
                'code':101,
                'message':'没有id'
            })

        try:
            item = Item.objects.prefetch_related('img').get(id=id)
        except Item.DoesNotExist:
            return Response({
                'code':102,
                'message':'物品不存在'
            })

        serializer = self.serializers_class(item)

        return Response({
            'code':0,
            'message':'获取成功',
            'data':serializer.data
        })

    @swagger_auto_schema(
        operation_summary="update the detail of the item",
        request_body=ItemSerializer,
        responses={
            200:ItemSerializer
        }
    )
    def put(self,request):
        id = request.data.get('id',None)

        if not id:
            return Response({
                'code': 101,
                'message': '没有id'
            })

        try:
            item = Item.objects.prefetch_related('img').get(id=id)
        except Item.DoesNotExist:
            return Response({
                'code': 102,
                'message': '物品不存在'
            })

        data = request.data
        images = request.data.getlist("img")

        new_data = {
            "name":data.get("name"),
            "description":data.get("description"),
            "count":data.get("count"),
            "price":data.get("price"),
            "owner":request.user.id,
            "img":[{"image":image} for image in images]
        }

        serializer = self.serializers_class(item,data=new_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({
            'code':0,
            'message':'修改成功',
            'data':serializer.data
        })

    @swagger_auto_schema(
        operation_summary="delte the item",
        manual_parameters=[openapi.Parameter(
            name="id",
            in_=openapi.IN_QUERY,
            description="the id of the item",
            type=openapi.TYPE_STRING
        )],
        responses={
            200:openapi.Response(description="base response")
        }
    )
    def delete(self,request):
        id = request.query_params.get("id",None)
        if not id:
            return Response({
                'code':101,
                'message':'没有id'
            })

        try:
            item = Item.objects.get(id=id)
            item.delete()
            return Response({
                'code':0,
                'message':'删除成功'
            })

        except Item.DoesNotExist:
            return Response({
                'code':102,
                'message':'物品不存在'
            })

class ItemListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = ItemSerializer


    @swagger_auto_schema(
        operation_summary="randomly get item list",
        responses={
            200:ItemSerializer(many=True)
        }
    )
    def get(self,request):
        user = request.user
        items = Item.objects.annotate(rand=Func(function='RAND',output_field=FloatField())).order_by('rand')[:20]
        serializer = self.serializer_class(items,many=True)

        return Response({
            'code':0,
            'message':"获取成功",
            'data':serializer.data
        })

class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = ItemCommentSerializer

    @swagger_auto_schema(
        operation_summary="upload the comment of the item",
        request_body=ItemCommentSerializer,
        responses={
            200:ItemCommentSerializer
        }
    )
    def post(self,request):
        user = request.user
        data = request.data

        if not Item.objects.filter(id=data.get("item_id")).exists():
            return Response({
                'code':101,
                'message':'物品不存在'
            })

        new_data = {
            "item":data.get("item_id"),
            "body":data.get("body"),
            "owner":user.id
        }

        serializer = self.serializer_class(data=new_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({
            'code':0,
            'message':'添加成功'
        })