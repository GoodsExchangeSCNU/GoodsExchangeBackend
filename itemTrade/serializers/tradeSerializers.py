from rest_framework import serializers

from ..models import Trade,User,ReviewForTrade,Item
from ..utils.errors import ValidationError


class TradeSerializer(serializers.ModelSerializer):
    """交易实例序列话器"""
    trade_id = serializers.UUIDField()
    user = serializers.IntegerField()

    FM = {
        1:{
            0:'buyer',
            2:'buyer',
            4:'seller'
        },
        2:{
            0:'buyer',
            4:'seller',
            3:'all'
        },
        3:{
            6:'seller'
        },
        6:{
            5:'buyer'
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

class CreateTradeSerializer(serializers.ModelSerializer):
    """新增trade实例"""
    user = serializers.IntegerField(required=True)

    class Meta:
        model = Trade
        fields = ['item','user']

    def create(self,validated_data):
        item = validated_data.get("item",None)
        user = validated_data.get("user",None)
        trade = Trade.objects.create(item=item,buyer_id=user,seller_id=item.owner.id)

        return trade

class CommentSerializer(serializers.ModelSerializer):
    """交易评论的序列号器"""

    class Meta:
        model = ReviewForTrade
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        return ReviewForTrade.objects.create(**validated_data)


class BuyerRoomListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = '__all__'
        extra_kwargs = {
            'id':{'read_only':True}
        }

    def to_representation(self, instance):
        item = instance.item
        other = instance.seller

        data = {
            'room_id':instance.id,
            'username':other.username,
            'item':{
                'name':item.name
            }
        }

        return data

class SellerRoomListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = '__all__'
        extra_kwargs = {
            'id':{'read_only':True}
        }

    def to_representation(self, instance):
        item = instance.item
        other = instance.buyer

        data = {
            'room_id':instance.id,
            'username':other.username,
            'item':{
                'name':item.name
            }
        }

        return data
