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

from rareapi.models.comment import Comment


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
                rare_user=rare_user,
                category=category,
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

    @action(methods=['POST'], detail=True)
    def createComment(self, request, pk=None):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        author = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=pk)

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            # Create a new Python instance of the Game class
            # and set its properties from what was sent in the
            # body of the request from the client.
            comment = Comment.objects.create(
                post=post,
                author=author,
                content=request.data["content"],
                created_on=datetime.date.today()
            )
            serializer = CommentSerializer(
                comment, context={'request': request})
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
            serializer = PostDetailSerializer(
                post, context={'request': request})
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

        # # Set the `joined` property on every post
        # for post in posts:
        #     # Check to see if the rare_user is in the attendees list on the post
        #     post.joined = rare_user in post.attendees.all()

        # Support filtering posts by post
        post = self.request.query_params.get('get_posts_by_user', None)
        if post is not None:
            posts = posts.filter(rare_user = rare_user)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username']


class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ['id', 'user']


class CommentSerializer(serializers.ModelSerializer):
    author = RareUserSerializer(many=False)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_on']
        depth: 1


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializer type
    """

    rare_user = RareUserSerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'image_url',
                  'content', 'rare_user', 'category')
        depth = 1


class PostDetailSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializer type
    """
    comments = CommentSerializer(many=True)
    rare_user = RareUserSerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'image_url',
                  'content', 'rare_user', 'category', 'comments')
        depth = 1
