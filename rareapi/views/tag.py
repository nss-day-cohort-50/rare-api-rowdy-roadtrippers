from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Tag

class TagView(ViewSet):
    def create(self):
        try:
            tag = Tag.objects.create(
                label=label
            )
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model: Tag
        fields: ('id', 'label')
        depth: 1
    