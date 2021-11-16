from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post
from django.contrib.auth import get_user_model
from rareapi.models import RareUser
from rareapi.models import Category
from rest_framework.decorators import action
import datetime



class PostView(ViewSet):
    """Rare Rowdy RoadTrippers"""

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

        category = Category.objects.get(pk=request.data["category_id"])

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            # Create a new Python instance of the Game class
            # and set its properties from what was sent in the
            # body of the request from the client.
            post = Post.objects.create(
                rare_user = rare_user,
                category = category,
                title=request.data["title"],
                publication_date=datetime.date.today(),
                image_url=request.data["image_url"],
                content=request.data["content"],
                approved=True
            )
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/posts/2
            #
            # The `2` at the end of the route becomes `pk`
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """
        rare_user = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["categoryId"])

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        post = Post.objects.get(pk=pk)
        post.rare_user = rare_user
        post.category = request.data["category"]
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = True

        post.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    # @action(methods=['get'], detail=False)
    def list(self, request):
        """Handle GET requests to posts resource

        Returns:
            Response -- JSON serialized list of posts
        """
        # Get the current authenticated user
        rare_user = RareUser.objects.get(user=request.auth.user)
        posts = Post.objects.all()

        # Set the `joined` property on every post
        for post in posts:
            # Check to see if the rare_user is in the attendees list on the post
            post.joined = rare_user in post.attendees.all()

        # Support filtering posts by post
        post = self.request.query_params.get('postId', None)
        if post is not None:
            posts = posts.filter(post__id=type)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)


    # @action(methods=['post', 'delete'], detail=True)
    # def signup(self, request, pk=None):
    #     """Managing gamers signing up for events"""
    #     # Django uses the `Authorization` header to determine
    #     # which user is making the request to sign up
    #     rare_user = RareUser.objects.get(user=request.auth.user)

    #     try:
    #         # Handle the case if the client specifies a game
    #         # that doesn't exist
    #         post = Post.objects.get(pk=pk)
    #     except Post.DoesNotExist:
    #         return Response(
    #             {'message': 'Event does not exist.'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     # A gamer wants to sign up for an event
    #     if request.method == "POST":
    #         try:
    #             # Using the attendees field on the event makes it simple to add a gamer to the event
    #             # .add(gamer) will insert into the join table a new row the gamer_id and the event_id
    #             post.attendees.add(post)
    #             return Response({}, status=status.HTTP_201_CREATED)
    #         except Exception as ex:
    #             return Response({'message': ex.args[0]})

    #     # User wants to leave a previously joined event
    #     elif request.method == "DELETE":
    #         try:
    #             # The many to many relationship has a .remove method that removes the gamer from the attendees list
    #             # The method deletes the row in the join table that has the gamer_id and event_id
    #             post.attendees.remove(rare_user)
    #             return Response(None, status=status.HTTP_204_NO_CONTENT)
    #         except Exception as ex:
    #             return Response({'message': ex.args[0]})
            
            
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializer type
    """
    # organizer = GamerSerializer(many=False)
    # joined = serializers.BooleanField(required=False)
    # game = GameSerializer()
    # attending_count = serializers.IntegerField(default=None)

    class Meta:
        model = Post
        fields = ('id', 'title', 'category')
        depth = 1