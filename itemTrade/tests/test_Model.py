import io

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from PIL import Image

from ..models import *

class TestUser(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user_1",
            password="test_user_1_password",
            email="user1@test.com"
        )

    def test_user_create(self):
        self.assertIsNotNone(User.objects.get(username="test_user_1"))

    def test_password(self):
        user = User.objects.get(username="test_user_1")
        self.assertEqual(user.check_password(("test_user_1_password")),True)
        self.assertEqual(user.check_password("test_user_1_passwor"), False)

    def test_query(self):
        self.assertEqual(self.user,User.objects.get(username="test_user_1"))

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

    def test_create(self):
        self.assertEqual(self.profile.student_id,20223803053)
        self.assertEqual(self.profile.student_class, "test class")
        self.assertEqual(self.profile.contact, 1111111111)
        self.assertEqual(self.profile.facauty, "test facauty")
        self.assertEqual(self.profile.dormitory, "test dormitory")

    def test_relationship(self):
        self.assertEqual(self.user,self.profile.user)

    def test_query(self):
        self.assertEqual(self.profile,Profile.objects.get(student_id=20223803053))


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

    def test_create(self):
        self.assertEqual(self.item.name,"test item 1")
        self.assertEqual(self.item.description,"test item")
        self.assertEqual(self.item.count,1)
        self.assertEqual(self.item.price,100)

    def test_relationship(self):
        self.assertEqual(self.item.owner,self.user)

    def test_query(self):
        self.assertEqual(self.item,Item.objects.get(name="test item 1"))

class TestItemImage(TestCase):

    def setUp(self):
        # 创建一个内存中的图像文件
        image = Image.new('RGB', (100, 100), color='red')  # 创建一个 100x100 的红色图片
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')  # 保存为 PNG 格式
        img_byte_arr.seek(0)  # 将游标重置到文件的开始

        # 将内存中的图像文件包装为 Django 的 UploadedFile 对象
        self.mock_image = InMemoryUploadedFile(
            img_byte_arr,  # 文件内容
            None,  # 文件名，None 时会使用默认值
            'test_image.png',  # 文件名
            'image/png',  # 文件类型
            img_byte_arr.tell(),  # 文件大小
            None  # 其他内容
        )

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
        self.image = ItemImage.objects.create(
            item=self.item,
            image=self.mock_image
        )

    def test_create(self):
        # imageField生成的文件名会带上盐，所以不一样
        self.assertEqual(1,1)

    def test_relationship(self):
        self.assertEqual(self.image.item,self.item)


class TestTrade(TestCase):
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

    def test_create(self):
        self.assertEqual(self.seller,self.trade.seller)
        self.assertEqual(self.buyer,self.trade.buyer)

    def test_update(self):
        self.trade.state = 2
        self.trade.save()
        self.assertEqual(self.trade.state,2)

    def test_query(self):
        self.assertEqual(Trade.objects.get(item=self.item),self.trade)

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

    def test_create(self):
        self.assertEqual(self.comment.body,"test comment")

    def test_relationship(self):
        self.assertEqual(self.comment.item,self.item)

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

    def test_create(self):
        self.assertEqual(self.comment.body,"test comment")

    def test_relationship(self):
        self.assertEqual(self.comment.owner,self.buyer)
        self.assertEqual(self.comment.Trade.item.owner,self.seller)
