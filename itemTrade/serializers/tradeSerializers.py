from enum import Enum
0
from rest_framework import serializers

from ..models import Trade,User,ReviewForTrade,Item
from ..utils.errors import ValidationError


class TradeSerializer(serializers.ModelSerializer):
    """交易实例序列话器"""
    trade_id = serializers.UUIDField()
    user = serializers.IntegerField()

    class UserType(Enum):
        BUYER  = 0
        SELLER = 1
        ALL = 2

    class CountOperate(Enum):
        PLUS = 0
        SUBTRACT = 1
        NONE = 2

    FM = {
        1:{
            0:(UserType.BUYER,CountOperate.NONE),
            2:(UserType.BUYER,CountOperate.SUBTRACT),
            4:(UserType.SELLER,CountOperate.NONE)
        },
        2:{
            0:(UserType.BUYER,CountOperate.PLUS),
            4:(UserType.SELLER,CountOperate.PLUS),
            3:(UserType.ALL,CountOperate.NONE)
        },
        3:{
            6:(UserType.SELLER,CountOperate.NONE)
        },
        6:{
            5:(UserType.BUYER,CountOperate.NONE)
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

        user_type = next_change[0]
        count_op = next_change[1]

        if user_type == self.UserType.BUYER and trade.buyer != user:
            raise ValidationError(code=105,detail="无法做出变化")
        elif user_type == self.UserType.SELLER and trade.seller != user:
            raise ValidationError(code=105, detail="无法做出变化")

        # 处理数量变化
        item = Item.objects.filter(trades__id=trade_id).first()
        if count_op == self.CountOperate.PLUS:
            item.count += 1
        elif count_op == self.CountOperate.SUBTRACT:
            if item.count < 1:
                raise ValidationError(code=106,detail="物品残余数量不足")
            item.count -= 1
        item.save()

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
