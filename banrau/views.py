from re import U
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.http import response
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view
from banrau import serializers

from banrau.models import Product, Category
from banrau.serializers import UserSerializer, GroupSerializer, ProductSerializer, CategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description_icontains= query))
        serializer = ProductSerializer(products, many = True)
        return response(serializer.data)
    else:
        return response({"products": []})

@api_view(['POST'])
def register(request):
    form = request.data
    # print(form)
    try:
        user = User.objects.create_user(
            username = form.get("username"),
            password = form.get("password"),
            email = form.get("email"),
        )
        serializers = UserSerializer(user, context={'request': None})
        return Response(serializers.data)
    except Exception as e:
        print(e)
        return Response({"error": "Tên tài khoản đã tồn tại"})

@api_view(['DELETE'])
def deleteAccount(request):
    username = request.data.get("username")
    try:
        user = User.objects.get(username = username)
        user.delete()
        return Response ({"message" : "Tài khoản của bạn đã được xóa"})
    except Exception as e:
        print (e)
        return Response({'error' : 500})

@api_view(['POST'])
def changePassword(request):
    username = request.data.get('username')
    oldPass = request.data.get('oldpassword')
    newPass = request.data.get('newpassword')
    try:
        user = User.objects.get(username = username)
        if not user.check_password(oldPass):
            return Response({'error' : 401, 'message' : 'Vui lòng nhập đúng mật khẩu'})
        user.set_password(newPass)
        return Response({'message' : 'Đổi mật khẩu thành công'})
    except Exception as e:
        print(e)
        return Response({'error' : 500})

@api_view(['POST'])
def updateUserProfile(request):
    form = request.data
    username = form.get("username")
    try:
        user = User.objects.get(username = username)
        user.first_name = form.get('first_name')
        user.last_name = form.get('last_name')
        user.email = form.get('email')
        user.save()
        return Response({'message' : 'Update Successful'}) 
    except Exception as e:
        print (e)
        return Response({'error' : 500})
    
