from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.

class Profile(models.Model):
    """Django内置user的附加属性"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.IntegerField(null=True,blank=True)
    student_class = models.CharField(max_length=50,null=True,blank=True)
    contact = models.IntegerField(null = True, blank=True)
    facauty = models.CharField(max_length=30, null=True, blank=True)
    dormitory = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"""
            contact: {self.contact}
            facauty: {self.facauty}
            dormitory: {self.dormitory}
            student_id: {self.student_id}
            student_class:{self.student_class}
        """
    
class Item(models.Model):
    """物品"""
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=50,null=True,blank=True)
    description = models.TextField(max_length=100,null=True,blank=True)
    count = models.IntegerField(default=1,null=True,blank=True)
    price = models.IntegerField(default=1,null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    models.ImageField()

    def __str__(self) -> str:
        return self.name
    
class ItemImage(models.Model):
    """储存单张图片"""
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    image = models.ImageField(upload_to='images/')
    item = models.ForeignKey(Item,on_delete=models.CASCADE, null=True, blank=True)

class Trade(models.Model):
    """交易实例"""
    States = (
        ('Code_0', '撤销'),
        ('Code_1', '初始化'),
        ('Code_2', '购买'),
        ('Code_3', '出售'),
        ('Code_4', '拒绝'),
        ('Code_5', '完成')
    )

    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sell_trade')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='buy_trade')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True, related_name='trades')
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=50, default='Code_1', choices=States)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    unReciveError = models.BooleanField(default=False)  # 买家未收到货时的异常状态

    def __str__(self):
        return f"Seller {self.seller.username}'s {self.item.name} Trade with {self.buyer}-------{self.state}"


class ReviewForItem(models.Model):
    """物品评论和留言"""
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    item = models.ForeignKey(Item,on_delete=models.CASCADE,null=True,blank=True,related_name="review")
    body = models.TextField(null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return f"{self.owner.username}'s comment for {self.item.name}"

class ReviewForTrade(models.Model):
    """交易的评论"""
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    Trade = models.OneToOneField(Trade, on_delete=models.CASCADE, null=True, blank=True, related_name="review")
    body = models.TextField(null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return f"{self.owner.username} comment"

class ChatMessage(models.Model):
    """聊天记录"""
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE,null=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    content = models.TextField(null=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"
