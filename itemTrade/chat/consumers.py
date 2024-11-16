import json, uuid
from django.core.serializers.json import DjangoJSONEncoder
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from asgiref.sync import sync_to_async
from itemTrade.models import Profile,ChatMessage,Trade,Item
from django.contrib.auth.models import User
from django.conf import settings
from django.core.cache import cache

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):  #当前端通过我们刚刚写的链接试图与我们建立连接时我们会执行这个函数
        self.userid = self.scope['url_route']['kwargs']['userid']
        await self.channel_layer.group_add(str(self.userid), self.channel_name)
        await self.accept()  #建立连接


    async def disconnet(self, close_code):
        print("disconnect")
        await self.channel_layer.group_discard(self.uuid, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            event = data['event']

            if event == 'fetchallchatrooms':
                chatroomidlist = await self.fetchallchatroomid(str(data['userid'])) #获取所有tradeid,一个tradeid对应一个聊天室
                chatroomlist = await self.getchatroomlist(data['userid']) #返回的是一个嵌套字典的列表[{'seller': seller_username, 'buyer':buyer_username,'item': item_name},]
                await self.addtogroups(chatroomidlist) #将用户group_add到他所拥有的chatroom中
                await self.channel_layer.group_send(
                    self.userid,
                    {
                        'type': 'fetch_allchatrooms',
                        'event': 'FetchChatroomlist',
                        'chatroomlist': chatroomlist
                        }
                )

            if event == 'sendnotice':
                buyer = await self.getmyusername(self.userid)
                await self.channel_layer.group_send(
                    str(data['another_userid']),
                    {
                        'type': 'send_notice',
                        'event': 'ReceiveNotice',
                        'content': f'{buyer}正向你发起聊天'
                    }
                )
                await self.send(text_data=json.dumps({
                    "event":"SendNoticeResponse",
                    "data":{
                        "code": 0,
                        "message": "发送成功",
                        "room_id":"",
                        "content":f"你已成功向{buyer}发起聊天"
                    }
                }))

            if event == 'sendmessage':
                await self.savemessage(data)
                sender = await self.getmyusername(self.userid)
                await self.channel_layer.group_send(
                    str(data['tradeid']),
                    {
                        'type': 'send_message',
                        'event': 'ReceiveMessage',
                        'sender': sender,
                        'content': data['content'],
                        'room_id': str(data['tradeid'])
                    }
                )

            if event == 'fetchmessage':
                history_messages = await self.getmessage(data['tradeid'])
                await self.channel_layer.group_send(
                    str(data['tradeid']),
                    {
                        'type': 'fetch_message',
                        'event': 'FetchMessage',
                        'history_messages': history_messages
                    }
                )



        except Exception as error:
            print(error)
            self.send_error_message(5000,error)

    async def addtogroups(self, chatroomidlist):
        for chatroomid in chatroomidlist:
            await self.channel_layer.group_add(str(chatroomid), self.channel_name)

    async def fetch_allchatrooms(self, data):
        await self.send(text_data=json.dumps(data))

    async def send_notice(self, data):
        await self.send(text_data=json.dumps(data))

    async def send_message(self, data):
        await self.send(text_data=json.dumps(data))

    async def fetch_message(self, data):
        await self.send(text_data=json.dumps(data))

    async def send_error_message(self,code,message):
        data = {
            "event": "error",
            "code": code,
            "message": message
        }
        await self.send(text_data=json.dumps(data))

    @sync_to_async
    def fetchallchatroomid(self, userid):
        try:
            user = User.objects.get(id=userid)
            trades_seller = user.sell_trade.all()
            trades_buyer = user.buy_trade.all()
            tradelist = []
            for trade in trades_seller:
                tradeid = trade.id
                tradelist.append(tradeid)
            for trade in trades_buyer:
                tradeid = trade.id
                tradelist.append(tradeid)

            return tradelist
        except User.DoesNotExist as error:
            self.send_error_message(4101,"用户不存在")
        
    @sync_to_async
    def getchatroomlist(self, userid):
        try:
            user = User.objects.get(id=userid)
            trades_seller = user.sell_trade.all()
            trades_buyer = user.buy_trade.all()
            chatroomlist = []
            for trade in trades_seller:
                buyer_username = trade.buyer.username
                chatroomlist.append({'type':'seller','seller':user.username, 'buyer':buyer_username,'item': trade.item.name, 'room_id':str(trade.id),'item_id':str(trade.item.id)})
            for trade in trades_buyer:
                seller_username = trade.seller.username
                chatroomlist.append({'type':'buyer','seller':seller_username, 'buyer':user.username,'item':trade.item.name,'room_id':str(trade.id),'item_id':str(trade.item.id)})

            return chatroomlist
        except User.DoesNotExist as error:
            self.send_error_message(4101,"用户不存在")

        
    @sync_to_async
    def getmyusername(self, userid):
        try:
            user = User.objects.get(id=userid)
            my_username = user.username
            return my_username
        except User.DoesNotExist as error:
            self.send_error_message(1,"用户不存在")
            self.close(code=4101)

    @sync_to_async
    def savemessage(self, data):
        try:
            trade = Trade.objects.get(id=data['tradeid'])
            sender = User.objects.get(id=self.userid)
            content = data['content']
            message = ChatMessage.objects.create(trade=trade, sender=sender, content=content)
        except Trade.DoesNotExist as error:
            self.send_error_message(4101,"目标用户不存在")
        except User.DoesNotExist as error:
            self.send_error_message(4201,"交易不存在")
        
    @sync_to_async
    def getmessage(self, tradeid):
        try:
            trade = Trade.objects.get(id=tradeid)
            history_messages = []

            messages = trade.chatmessage_set.all()
            for message in messages:
                sender = message.sender
                history_messages.append({'sender':sender.username, 'content':message.content})
            return history_messages
        except Trade.DoesNotExist as error:
            self.send_error_message(2,"交易不存在")
            return []





