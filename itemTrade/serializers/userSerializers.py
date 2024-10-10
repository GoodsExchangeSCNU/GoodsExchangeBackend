from rest_framework import serializers
from ..models import User,Profile,ItemImage,Trade,Item

from ..utils.errors import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    """注册用模型"""
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username','password','confirm_password']

        extra_kwargs = {
            'username': {'validators': []},
        }

    def validate_username(self,value):
        """检查用户名是否存在"""
        if User.objects.filter(username=value).exists():
            raise ValidationError(101, "Username already exists")
        return value

    def validate(self, data):
        """检查password和repassword是否相等"""
        if data['password'] != data['confirm_password']:
            raise ValidationError(102, "Passwords do not match")

        return data

    def create(self, validated_data):
        # 删除确认密码字段
        del validated_data['confirm_password']
        user = User.objects.create_user(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()

        Profile.objects.create(user=user)

        return user

class ProfileSerializer(serializers.ModelSerializer):
    """详细信息序列化"""

    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'student_id':{'required':False},
            'student_class':{'required':False},
            'contact':{'required':False},
            'facauty':{'required':False},
            'dormitory':{'required':False}
        }


class UserSerializer(serializers.ModelSerializer):
    """用户序列化模型"""
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id','username', 'email','profile']
        # 这里将profile的字段都设置出来，为了让创建和更新的时候可以不嵌套
        extra_kwargs = {
            'id':{'required':False,'read_only':True},
            'username':{'required':False},
            'email':{'required':False}
        }

    def update(self, instance:User, validated_data:dict):
        """更新用户信息"""
        profile_data = validated_data.pop("profile", None)
        instance.username = validated_data.get("username",instance.username)
        instance.email = validated_data.get("email",instance.email)
        instance.save()

        if profile_data is not None:
            profile,created = Profile.objects.get_or_create(user=instance)
            profile.student_id = profile_data.get("student_id",profile.student_id)
            profile.student_class = profile_data.get("student_class", profile.student_class)
            profile.contact = profile_data.get("contact", profile.contact)
            profile.facauty = profile_data.get("facauty", profile.facauty)
            profile.dormitory = profile_data.get("dormitory", profile.dormitory)
            profile.save()

        return instance

class RecordUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class RecordItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['img','name','price']

class RecordSerializer(serializers.ModelSerializer):
    """交易记录序列化模型"""
    seller = RecordUserSerializer()
    buyer = RecordUserSerializer()
    item = RecordItemSerializer()

    class Meta:
        model = Trade
        fields = ['id','state','seller','buyer','item']
