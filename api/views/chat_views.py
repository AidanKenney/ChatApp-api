from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.chat import Chat
from ..serializers import ChatSerializer, UserSerializer

# Create your views here.
class Chats(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = ChatSerializer
    def get(self, request):
        """Index request"""
        # Get all the chats:
        # chats = Chat.objects.all()
        # Filter the chats by owner, so you can only see your owned chats
        chats = Chat.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = ChatSerializer(chats, many=True).data
        return Response({ 'chats': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['chat']['owner'] = request.user.id
        # Serialize/create chats
        chat = ChatSerializer(data=request.data['chat'])
        # If the chat data is valid according to our serializer...
        if chat.is_valid():
            # Save the created mango & send a response
            chat.save()
            return Response({ 'chat': chat.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(chat.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the chat to show
        chat = get_object_or_404(Chat, pk=pk)
        # Only want to show owned chats?
        if not request.user.id == chat.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this chat')

        # Run the data through the serializer so it's formatted
        data = ChatSerializer(chat).data
        return Response({ 'chat': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate chat to delete
        chat = get_object_or_404(Chat, pk=pk)
        # Check the chat's owner agains the user making this request
        if not request.user.id == chat.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this mango')
        # Only delete if the user owns the chats
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['chats'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['chat'].get('owner', False):
            del request.data['chat']['owner']

        # Locate Chat
        # get_object_or_404 returns a object representation of our Chat
        chat = get_object_or_404(Chat, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == chat.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this mango')

        # Add owner to data object now that we know this user owns the resource
        request.data['chat']['owner'] = request.user.id
        # Validate updates with serializer
        data = ChatSerializer(chat, data=request.data['chat'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
