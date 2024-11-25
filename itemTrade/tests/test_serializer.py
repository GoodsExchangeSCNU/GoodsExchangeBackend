from django.test import TestCase

from ..serializers.userSerializers import *
from ..serializers.itemSerializers import *
from ..models import *

class TestUserSerializer(TestCase):
    serializer_class = UserSerializer
    def setUp(self):
        self.User = User.objects.create_user(
            username="test_user_1",
            password="test_user_1_password",
            email="user1@test.com"
        )
        self.serializer = UserSerializer(instance=self.User)
    def test_UserSerializer(self):
        serialized_data = self.serializer.data
        expected_data = {
            'id': self.User.id,
            'username': "test_user_1",
            'email': "user1@test.com",
            'profile': None

        }
        self.assertEqual(serialized_data, expected_data)

class TestProfile(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user_1",
            password="test_user_1_password",
            email="user1@test.com"
        )

        self.profile = Profile.objects.create(
            user = self.user,
            student_id=20223803053,
            student_class="test class",
            contact=1111111111,
            facauty="test facauty",
            dormitory="test dormitory",
        )
    
        self.serializer = ProfileSerializer(instance=self.profile)
    def test_ProfileSerializer(self):
        serialized_data = self.serializer.data
        expected_data = {
            'id': self.user.id,
            'student_id':20223803053,
            'student_class':"test class",
            'contact':1111111111,
            'facauty':"test facauty",
            'dormitory':"test dormitory",
            'created': self.profile.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'user': self.user.id
        }
        self.assertEqual(serialized_data, expected_data)

class TestItem(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user_1",
            password="test_user_1_password",
            email="user1@test.com"
        )
        self.item = Item.objects.create(
            owner=self.user,
            name="test item 1",
            description="test item",
            count=1,
            price=100
        )

    def test_ItemSerializer(self):
        self.serializer = ItemSerializer(instance=self.item)
        serialized_data = self.serializer.data
        expected_data = {
            'id':str(self.item.id),
            'name':"test item 1",
            'description':"test item",
            'owner':self.user.id,
            'count':1,
            'price':100,
            'img':[]
        }

        self.assertEqual(serialized_data, expected_data)

class TestTradeSerializer(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(
            username="test_user_buyer",
            password="test_user_buyer_password",
            email="user_buyer@test.com"
        )
    
        self.seller = User.objects.create_user(
            username="test_user_seller",
            password="test_user_seller_password",
            email="user_seller@test.com"
        )
        self.item = Item.objects.create(
            owner=self.seller,
            name="test item 1",
            description="test item",
            count=1,
            price=100
        )
        self.trade = Trade.objects.create(
            seller=self.seller,
            buyer=self.buyer,
            item=self.item
        )
    
    def test_TradeSerializer_buyer(self):
        self.serializer = UserSerializer(instance=self.buyer)
        serialized_data = self.serializer.data
        expected_data = {
            'id': self.buyer.id,
            'username': "test_user_buyer",
            'email': "user_buyer@test.com",
            'profile': None
        }
        self.assertEqual(serialized_data, expected_data)

    def test_TradeSerializer_seller(self):
        self.serializer = UserSerializer(instance=self.seller)
        serialized_data = self.serializer.data
        expected_data = {
            'id': self.seller.id,
            'username': "test_user_seller",
            'email': "user_seller@test.com",
            'profile': None
        }
        self.assertEqual(serialized_data, expected_data)

    def test_ItemSerializer(self):
        self.serializer = ItemSerializer(instance=self.item)
        serialized_data = self.serializer.data
        expected_data = {
            'id':str(self.item.id),
            'name':"test item 1",
            'description':"test item",
            'owner':self.seller.id,
            'count':1,
            'price':100,
            'img':[]
        }

        self.assertEqual(serialized_data, expected_data)

class TestReviewForItem(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user_1",
            password="test_user_1_password",
            email="user1@test.com"
        )
        self.item = Item.objects.create(
            owner=self.user,
            name="test item 1",
            description="test item",
            count=1,
            price=100
        )
        self.comment = ReviewForItem.objects.create(
            owner=self.user,
            item=self.item,
            body="test comment"
        )

    def test_ReviewForItemSerializer(self):
        self.serializer = ItemCommentSerializer(instance=self.comment)
        serialized_data = self.serializer.data
        expected_data = {
            'id':str(self.comment.id),
            'body': "test comment",
            'create_at': self.comment.create_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'owner': self.user.id,
            'item': self.item.id
        }
        self.assertEqual(serialized_data, expected_data)

class TestReviewForTrade(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(
            username="test_user_buyer",
            password="test_user_buyer_password",
            email="user_buyer@test.com"
        )
        self.seller = User.objects.create_user(
            username="test_user_seller",
            password="test_user_seller_password",
            email="user_seller@test.com"
        )
        self.item = Item.objects.create(
            owner=self.seller,
            name="test item 1",
            description="test item",
            count=1,
            price=100
        )
        self.trade = Trade.objects.create(
            seller=self.seller,
            buyer=self.buyer,
            item=self.item
        )

        self.comment = ReviewForTrade.objects.create(
            owner=self.buyer,
            Trade=self.trade,
            body="test comment"
        )
     
    def test_ReviewForTradeSerializer(self):
        self.serializer = ItemCommentSerializer(instance=self.comment)
        serialized_data = self.serializer.data
        expected_data = {
            'id':str(self.comment.id),
            'body': "test comment",
            'create_at': self.comment.create_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'owner': self.buyer.id,
            'item': None
        }
        self.assertEqual(serialized_data, expected_data)
       
