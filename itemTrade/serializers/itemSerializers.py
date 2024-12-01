import datetime

from rest_framework import serializers


from ..models import Item,ItemImage,ReviewForItem,User
from ..utils.errors import ValidationError
from ..serializers.userSerializers import UserSerializer

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ['image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        return representation["image"]

class ItemCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewForItem
        fields = '__all__'


    def create(self, validated_data):
        item = validated_data.get('item')
        body = validated_data.get('body')
        owner = validated_data.get('owner')

        review = ReviewForItem.objects.create(item=item,body=body,owner=owner)
        return review

    def to_representation(self, instance):
        representation_data = super().to_representation(instance)
        create_at = representation_data.get("create_at")
        owner = representation_data.get("owner")
        if create_at:
            create_at = datetime.datetime.fromisoformat(create_at.replace("Z","+00:00"))
            representation_data["create_at"] = int(create_at.timestamp() * 1000)

        if owner:
            owner = User.objects.get(id=owner)
            representation_data["owner"] = owner.username

        return representation_data

class ItemSerializer(serializers.ModelSerializer):
    """物品类序列化模型"""
    img = ImageSerializer(many=True)
    review = ItemCommentSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Item
        fields = ['id','name','owner','description','count','price','img','review']
        extra_kwargs = {
            'id':{'required':False,'read_only':True},
            'name': {'required': True},
            'description': {'required': True},
            'owner': {'required': True},
            'count': {'required': True},
            'price': {'required': True},
            'review':{'required':False,'read_only':True}
        }

    def create(self, validated_data):
        imgs = validated_data.pop('img',None)
        item = Item.objects.create(**validated_data)
        item.save()

        if imgs is not None:
            for img in imgs:
                ItemImage.objects.create(image=img["image"],item=item)

        return item

    def update(self,instance,validated_data):
        imgs = validated_data.pop('img',None)

        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.count = validated_data.get('count',instance.count)
        instance.price = validated_data.get('price',instance.price)
        instance.save()

        if imgs:
            for img in imgs:
                ItemImage.objects.create(image=img["image"],item=instance)

        instance.refresh_from_db()
        return instance

    def to_representation(self, instance):
        representation_data = super().to_representation(instance)

        try:
            user = User.objects.get(id=representation_data.get('owner',None))
            owner = UserSerializer(user)
            representation_data['user'] = owner.data
        except User.DoesNotExist as e:
            pass

        return representation_data

