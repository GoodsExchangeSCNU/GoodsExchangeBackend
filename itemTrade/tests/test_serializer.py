from django.test import TestCase

from ..serializers.userSerializers import *
from ..models import *

class TestUserSerializer(TestCase):
    serializer_class = UserSerializer
    def test_CreateUser(self):
        pass