from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models.mango import Mango
from .models.user import User
from .models.post import Post
from .models.comment import Comment
from .models.vote import Vote

class MangoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mango
        fields = ('id', 'name', 'color', 'ripe', 'owner')

class UserSerializer(serializers.ModelSerializer):
    # This model serializer will be used for User creation
    # The login serializer also inherits from this serializer
    # in order to require certain data for login
    class Meta:
        # get_user_model will get the user model (this is required)
        # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#referencing-the-user-model
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = { 'password': { 'write_only': True, 'min_length': 5 } }

    # This create method will be used for model creation
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserRegisterSerializer(serializers.Serializer):
    # Require email, password, and password_confirmation for sign up
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        # Ensure password & password_confirmation exist
        if not data['password'] or not data['password_confirmation']:
            raise serializers.ValidationError('Please include a password and password confirmation.')

        # Ensure password & password_confirmation match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Please make sure your passwords match.')
        # if all is well, return the data
        return data

class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'owner', 'post', 'created_at', 'updated_at')

class UserReadSerializer(serializers.ModelSerializer):
    # This model serializer will be used for User creation
    # The login serializer also inherits from this serializer
    # in order to require certain data for login
    class Meta:
        # get_user_model will get the user model (this is required)
        # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#referencing-the-user-model
        model = get_user_model()
        fields = ('id', 'email', 'password', 'posts', 'comments')
        extra_kwargs = { 'password': { 'write_only': True, 'min_length': 5 } }

class CommentReadSerializer(serializers.ModelSerializer):
    owner = UserReadSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'content', 'owner', 'post', 'created_at', 'updated_at')

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'up_or_down', 'owner', 'post', 'created_at', 'updated_at')

class VoteReadSerializer(serializers.ModelSerializer):
    owner = UserReadSerializer(read_only=True)
    class Meta:
        model = Vote
        fields = ('id', 'up_or_down', 'owner', 'post', 'created_at', 'updated_at')

class PostSerializer(serializers.ModelSerializer):
    comments = CommentReadSerializer(many=True, read_only=True)
    # owner = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'owner', 'comments', 'votes', 'created_at', 'updated_at')

class PostReadSerializer(serializers.ModelSerializer):
    comments = CommentReadSerializer(many=True, read_only=True)
    owner = UserReadSerializer(read_only=True)
    votes = VoteReadSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'owner', 'comments', 'votes', 'created_at', 'updated_at')
