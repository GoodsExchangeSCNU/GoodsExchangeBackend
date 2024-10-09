from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny

from ..models import Trade
from ..serializers.tradeSerializers import TradeSerializer, CommentSerializer, RoomListSerializer


class TradeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = TradeSerializer

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


class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = CommentSerializer

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

    serializer_class = RoomListSerializer

    def get(self,request):
        user = request.user

        buyerList = user.buy_trade.all()
        sellerList = user.sell_trade.all()

        buyerSerializers = None
        sellerSerializers = None

        if buyerList:
            buyerList = [{
                "room_id":trade.id,
                "username":trade.seller.username,
                "item":trade.item.to_dict()
            }
                         for trade in buyerList]

            buyerSerializers = self.serializer_class(data=buyerList,many=True)

        if sellerList:
            sellerList = [{
                "room_id":trade.id,
                "username":trade.buyer.username,
                "item":trade.item.to_dict()
            }
                         for trade in sellerList]

            sellerSerializers = self.serializer_class(data=sellerList,many=True)

        if (not buyerSerializers or buyerSerializers.is_valid(raise_exception=True))\
                and\
            (not sellerSerializers or sellerSerializers.is_valid(raise_exception=True)):
            return Response({
                'code':0,
                'message':'获取成功',
                'data':{
                    'buyer':buyerSerializers.data if buyerSerializers else None,
                    'seller':sellerSerializers.data if sellerSerializers else None
                }
            })
