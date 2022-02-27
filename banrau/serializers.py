from django.contrib.auth.models import User, Group
from rest_framework import serializers

from banrau.models import Product, Category


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = []


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = []
