from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import Trade,Item
from ..serializers.tradeSerializers import TradeSerializer, CommentSerializer, BuyerRoomListSerializer,SellerRoomListSerializer, CreateTradeSerializer


class TradeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = TradeSerializer

    @swagger_auto_schema(
        operation_summary="update the trade state",
        request_body=TradeSerializer,
        responses={
            200: TradeSerializer
        }
    )
    def put(self,request):
        trade_id = request.data.pop('trade_id')
        state = request.data.get('state',None)
        if not trade_id:
            return Response({
                'code':101,
                'message':'交易id为空'
            })

        if not state:
            return Response({
                'code':102,
                'message':'更新状态为空'
            })

        try:
            trade = Trade.objects.get(id=trade_id)
        except Trade.DoesNotExist:
            return Response({
                'code':103,
                'message':'交易不存在'
            })

        new_data = {
            'trade_id':trade_id,
            'user':request.user.id,
            'state':request.data.get('state', None)
        }

        serializer = self.serializer_class(trade,data=new_data)
        if serializer.is_valid():
            serializer.save()

        return Response({
            'code':0,
            'message':'修改成功'
        })

    @swagger_auto_schema(
        operation_summary="create a trade",
        request_body=CreateTradeSerializer,
        responses={
            200: openapi.Response(description="base response")
        }
    )
    def post(self,request):
        data = {
            'user':request.user.id,
            'item':request.data.get('item_id',None)
        }
        print(data)
        if not data['item'] or not Item.objects.filter(id=data['item']).exists():
            return Response({
                'code':101,
                'message':'物品不存在'
            })

        serializer = CreateTradeSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            'code':0,
            'message':'添加成功'
        })


class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = CommentSerializer

    @swagger_auto_schema(
        operation_summary="create a comment for trade",
        request_body=CommentSerializer,
        responses={
            200: CommentSerializer
        }
    )
    def put(self, request):
        trade_id = request.data.get('trade_id',None)
        body = request.data.get('body',None)
        owner = request.user.id

        if not Trade.objects.filter(id=trade_id).exists():
            return Response({
                'code':101,
                'message':'交易不存在'
            })

        data = {
            'Trade':trade_id,
            'body':body,
            'owner':owner
        }

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({
            'code':0,
            'message':'修改成功',
            'data':serializer.data
        })


class RoomListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_summary="return a list of trade which relevant to the user ",
        responses={
            200: BuyerRoomListSerializer
        }
    )
    def get(self,request):
        user = request.user

        buyerList = user.buy_trade.all()
        sellerList = user.sell_trade.all()

        buyerSerializers = BuyerRoomListSerializer(buyerList,many=True)
        sellerSerializers = SellerRoomListSerializer(sellerList,many=True)

        return Response({
            'code':0,
            'message':'获取成功',
            'data':{
                'buyer':buyerSerializers.data if buyerSerializers else None,
                'seller':sellerSerializers.data if sellerSerializers else None
            }
        })
