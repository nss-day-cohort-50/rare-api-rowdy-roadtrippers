"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Category
from rareapi.models import RareUser
from django.core.exceptions import ValidationError
from rest_framework import status

class CategoryView(ViewSet):
    """Rare Categories"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        rare_user = RareUser.objects.get(user=request.auth.user)

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `gameTypeId` in the body of the request.

        # category = Category.objects.get(pk=request.data["category_id"])

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            # Create a new Python instance of the Game class
            # and set its properties from what was sent in the
            # body of the request from the client.
            category = Category.objects.create(
                # rare_user = rare_user,
                label = request.data["label"]
            )
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single category

        Returns:
            Response -- JSON serialized category
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all categories

        Returns:
            Response -- JSON serialized list of game types
        """
        categories = Category.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for game types

    Arguments:
        serializers
    """
    class Meta:
        model = Category
        fields = ('id', 'label')