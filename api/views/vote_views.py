from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.vote import Vote
from ..serializers import VoteSerializer, VoteReadSerializer

# Create your views here.
class Votes(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = VoteSerializer
    def get(self, request):
        """Index request"""
        # Get all the posts:
        # posts = Post.objects.all()
        # Filter the posts by owner, so you can only see your owned posts
        votes = Vote.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = VoteReadSerializer(votes, many=True).data
        return Response({ 'votes': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['vote']['owner'] = request.user.id
        # Serialize/create posts
        vote = VoteSerializer(data=request.data['vote'])
        # If the posts data is valid according to our serializer...
        if vote.is_valid():
            # Save the created mango & send a response
            vote.save()
            return Response({ 'vote': vote.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(vote.errors, status=status.HTTP_400_BAD_REQUEST)

class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the post to show
        vote = get_object_or_404(Vote, pk=pk)
        # Only want to show owned Post?
        if not request.user.id == vote.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this comment')

        # Run the data through the serializer so it's formatted
        data = VoteReadSerializer(vote).data
        return Response({ 'vote': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate post to delete
        vote = get_object_or_404(Vote, pk=pk)
        # Check the post's owner agains the user making this request
        if not request.user.id == vote.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this comment')
        # Only delete if the user owns the posts
        vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['posts'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['vote'].get('owner', False):
            del request.data['vote']['owner']

        # Locate Post
        # get_object_or_404 returns a object representation of our Post
        vote = get_object_or_404(Vote, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == vote.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this comment')

        # Add owner to data object now that we know this user owns the resource
        request.data['vote']['owner'] = request.user.id
        # Validate updates with serializer
        data = VoteReadSerializer(vote, data=request.data['vote'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
