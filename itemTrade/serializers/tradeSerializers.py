from rest_framework import serializers

from ..models import Trade,User,ReviewForTrade,Item
from ..utils.errors import ValidationError


class TradeSerializer(serializers.ModelSerializer):
    """交易实例序列话器"""
    trade_id = serializers.UUIDField()
    user = serializers.IntegerField()

    FM = {
        'Code_1':{
            'Code_0':'buyer',
            'Code_2':'buyer',
            'Code_4':'seller'
        },
        'Code_2':{
            'Code_0':'buyer',
            'Code_4':'seller',
            'Code_3':'all'
        },
        'Code_3':{
            'Code_6':'seller'
        },
        'Code_6':{
            'Code_5':'buyer'
        }
    }

    class Meta:
        model = Trade
        fields = ['trade_id','state','user']

    def validate(self,data):
        """验证状态变化是否符合逻辑"""

        trade_id = data.get('trade_id',None)
        user_id = data.get('user',None)
        state = data.get('state',None)


        try:
            user = User.objects.get(id=user_id)
            trade = Trade.objects.get(id=trade_id)
        except User.DoesNotExist:
            raise ValidationError(code=104,detail="用户不存在")
        except Trade.DoesNotExist:
            raise ValidationError(code=103,detail="交易不存在")

        next_change = self.FM.get(trade.state,None)
        if not next_change:
            raise ValidationError(code=105,detail="无法做出变化")
        next_change = next_change.get(state,None)
        if not next_change:
            raise ValidationError(code=105,detail="无法做出变化")

        if next_change == "buyer" and trade.buyer != user:
            raise ValidationError(code=105,detail="无法做出变化")
        elif next_change == "seller" and trade.seller != user:
            raise ValidationError(code=105, detail="无法做出变化")

        return data

    def update(self,instance,validated_data):
        print(validated_data)
        instance.state = validated_data.get('state',instance.state)
        instance.save()

        return instance

class CommentSerializer(serializers.ModelSerializer):
    """交易评论的序列号器"""

    class Meta:
        model = ReviewForTrade
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        return ReviewForTrade.objects.create(**validated_data)

class DisplayItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'

    def to_representation(self, instance):

        return {
            'name':instance.get('name',None)
        }


class RoomListSerializer(serializers.Serializer):
    """聊天室序列化器"""
    room_id = serializers.UUIDField()
    username = serializers.CharField()
    item = DisplayItemSerializer()

    class Meta:
        fields = ['room_id','username','item']

