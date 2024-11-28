from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Func, FloatField

from ..models import Item
from ..serializers.itemSerializers import ItemSerializer

class RecommandView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        items = Item.objects.annotate(rand=Func(function='RAND',output_field=FloatField())).order_by('rand')[:20]
        serializer = ItemSerializer(items,many=True)

        return Response({
            'code':0,
            'message':"获取成功",
            'data':serializer.data
        })


class SearchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        key = request.data.get("key",None)
        if not key:
            return Response({
                'code':102,
                'message':"没有key"
            })

        try:
            items = Item.objects.filter(name__icontains=key).filter(description__icontains=key).all()[:20]
            serializer = ItemSerializer(items,many=True)
        except Item.DoesNotExist as e:
            return Response({
                'code':103,
                'message':"没有找到任何匹配项"
            })

        return Response({
            'code':0,
            'message':"获取成功",
            'data':serializer.data
        })
