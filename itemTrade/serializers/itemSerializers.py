from rest_framework import serializers


from ..models import Item,ItemImage,ReviewForItem
from ..utils.errors import ValidationError
from ..serializers.userSerializers import UserSerializer

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ['image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        return representation["image"]

class ItemSerializer(serializers.ModelSerializer):
    """物品类序列化模型"""
    img = ImageSerializer(many=True)
    owner = UserSerializer()

    class Meta:
        model = Item
        fields = ['id','name','owner','description','count','price','img']
        extra_kwargs = {
            'id':{'required':False,'read_only':True},
            'name': {'required': True},
            'description': {'required': True},
            'owner': {'required': True},
            'count': {'required': True},
            'price': {'required': True}
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

class ItemCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewForItem
        fields = '__all__'


    def create(self, validated_data):
        item = validated_data.get('item')
        body = validated_data.get('body')
        owner = validated_data.get('owner')
        print(item)

        review = ReviewForItem.objects.create(item=item,body=body,owner=owner)
        return review
