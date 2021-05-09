from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Post, Contact
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.conf import settings

# step1: Import user from django , creating user serializer

# step6: Import post from api.models and create PostSerializer
# To add Post model to the API we need to follow the similar process as we did for user

# step7: The many-to-one relationship between posts and users was defined by
# the Post model in the previous step so we just added here to maintain relation.


class PostSerializer(serializers.ModelSerializer):  # step6
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

    def create(self, validated_data):
        subject = f"message from {validated_data['email']}"
        message = f"{validated_data['message']}"
        from_email = settings.FROM_EMAIL
        recipient_list = [settings.TO_EMAIL, ]
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):  # step1 ---> step2 views.py
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # step7

    class Meta:
        model = User
        fields = ['id', 'username', 'posts']

# The PrimaryKeyRelatedField represents the list of posts in this many-to-one relationship
# (many=True signifies there is more than one post). ---> create views for PostAPI on step8


class RegisterSerializersModel(ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            "password": {
                'write_only': True
            }
        }

    def create(self, validated_data):
        account = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password!= password2:
            raise serializers.ValidationError({'password': 'Password must match.'})
        account.set_password(password)
        account.save()
        return account

# for user to change password


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
