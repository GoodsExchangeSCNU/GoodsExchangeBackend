from rest_framework import serializers
from ..models import User,Profile,ItemImage

class UserSerializer(serializers.ModelSerializer):
    """用户序列化模型"""
    student_id = serializers.CharField(required=False, allow_blank=True)
    student_class = serializers.CharField(required=False, allow_blank=True)
    contact = serializers.CharField(required=False, allow_blank=True)
    facauty = serializers.CharField(required=False, allow_blank=True)
    dormitory = serializers.CharField(required=False, allow_blank=True)


    class Meta:
        model = User
        fields = ['username','password', 'email','student_id','student_class','contact','facauty','dormitory','id']
        # 这里将profile的字段都设置出来，为了让创建和更新的时候可以不嵌套
        extra_kwargs = {
            'username':{'required':True},
            'password':{'write_only':True,'required':True},
            'email':{'required':False,'write_only':True},
            'student_id':{'required':False,'write_only':True},
            'student_class':{'required':False,'write_only':True},
            'contact':{'required':False,'write_only':True},
            'facauty':{'required':False,'write_only':True},
            'dormitory':{'required':False,'write_only':True}
        }

    def __init__(self,*args, **kwargs):
        
        # 如果是修改操作，用户名和密码不是必须的
        instance = args[0] if len(args) > 0 else None
        if isinstance(instance,User):
            self.fields['username'].required = False
            self.fields['password'].required = False

        return super().__init__(*args,**kwargs)

    def to_representation(self, instance):
        """重写序列化,让显示不嵌套"""
        representation = super().to_representation(instance)
        profile = instance.profile
        representation['student_id'] = profile.student_id
        representation['student_class'] = profile.student_class
        representation['contact'] = profile.contact
        representation['facauty'] = profile.facauty
        representation['dormitory'] = profile.dormitory

        return representation

    def create(self, validated_data):
        """创建新用户"""
        stu_id = validated_data.pop('student_id', None)
        stu_class = validated_data.pop('student_class', None)
        contact = validated_data.pop('contact', None)
        facauty = validated_data.pop('facauty',None)
        dormitory = validated_data.pop('dormitory',None)
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        if stu_class or stu_id or contact or facauty or dormitory:
            Profile.objects.create(student_id=stu_id,student_class=stu_class,contact=contact,facauty=facauty,dormitory=dormitory,user=user)

        return user

    def update(self, instance:User, validated_data:dict):
        """更新用户信息"""
        stu_id = validated_data.pop('student_id',None)
        stu_class = validated_data.pop('student_class',None)
        contact = validated_data.pop('contact', None)
        facauty = validated_data.pop('facauty',None)
        dormitory = validated_data.pop('dormitory',None)
        
        if stu_id or stu_class or contact or facauty or dormitory:
            profile,created = Profile.objects.get_or_create(user=instance)
            profile.student_id = stu_id if stu_id else profile.student_id
            profile.student_class = stu_class if stu_class else profile.student_class
            profile.contact = contact if contact else profile.contact
            profile.facauty = facauty if facauty else profile.facauty
            profile.dormitory = dormitory if dormitory else profile.dormitory

        
            profile.save()
        
        instance.username = validated_data.get("uswrname",instance.username)
        instance.email = validated_data.get("email",instance.email)

        instance.save()

        return instance

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemImage
        fields = '__all__'
