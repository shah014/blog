from rest_framework import generics
from api import serializers
from django.contrib.auth.models import User
from api.models import Post, Contact
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from .serializers import RegisterSerializersModel, ChangePasswordSerializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import status

# step2: Using generics view class, created API View class
# i.e, ListAPIView and RetrieveAPIView --> step3 api/urls.py
# step8: Creating a set of views for the Post API
# step9: For convenience, we can add a Log in button to the browsable API
# by adding the following path to url_patterns
# step11: Adding permission_classes


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
# ListAPIView provides read-only access via get to list of users


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
# RetrieveAPIView provides read-only access via get to single user


class PostList(generics.ListCreateAPIView):  # step8 ---> url
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # step11: adding permission classes
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('id', 'owner', )
    filterset_fields = ('id', 'owner', )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):  # step8
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]  # step11: Adding permission classes

# Step11: details --->add urls to views
# 1.the PostList view needs only the IsAuthenticatedOrReadOnly permission because
# a user must be authenticated to create a post, and any user can view the list of posts.
# 2.The PostDetail requires both permissions, as updating and destroying a post should only
# be allowed for an authenticated user who is also the owner of the post. Retrieving a single
# post is read-only and does not require any permissions.



def registration_view(request):
    ser = RegisterSerializersModel(data=request.data)
    data = {}
    if ser.is_valid():
        account = ser.save()
    else:
        data = ser.errors
    return Response(ser.data)


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializersModel
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class RegisterUser(CreateAPIView):
    serializer_class = RegisterSerializersModel
    queryset = User.objects.all()


# APIView for updating password
class UpdatePassword(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"message": "Successfully updated"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactCreate(generics.CreateAPIView):  # step8 ---> url
    queryset = Contact.objects.all()
    serializer_class = serializers.ContactSerializer
    permission_classes = [AllowAny]  # step11: adding permission classes


