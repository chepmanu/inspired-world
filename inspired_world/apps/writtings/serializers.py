import re

from inspired_world.apps.profiles.serializers import ProfileSerializer
from rest_framework import serializers
from .models import Writting, Tag
from .tag_relations import TagRelatedField


class WrittingSerializer(serializers.ModelSerializer):
    """
    Defines the article serializer
    """
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    slug = serializers.SlugField(required=False)
    image_url = serializers.URLField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    author = ProfileSerializer(read_only=True)
    tagList = TagRelatedField(many=True, required=False, source='tags')

    class Meta:
        model = Writting
        fields = ['id', 'title', 'slug', 'body',
                  'description', 'image_url', 'created_at',
                  'updated_at', 'tagList', 'author']

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])

        writting = Writting.objects.create(**validated_data)

        for tag in tags:
            writting.tags.add(tag)

        return writting

    def validate(self, data):
        # The `validate` method is used to validate the title,
        # description and body
        title = data.get('title', None)
        description = data.get('description', None)
        # Validate title is not a series \
        # of symbols or non-alphanumeric characters
        if re.match(r"[!@#$%^&*~\{\}()][!@#$%^&*~\{\}()]{2,}", title):
            raise serializers.ValidationError(
                "A title must not contain two symbols/foreign \
                characters following each other"
            )
        # Validate the description is not a series of symbols or
        # non-alphanumeric characters
        if re.match(r"[!@#$%^&*~\{\}()][!@#$%^&*~\{\}()]{2,}", description):
            raise serializers.ValidationError(
                """
                A description must not contain two symbols/foreign \
                characters following each other
                """
            )
        return data


class TagSerializer(serializers.ModelSerializer):
    """
    Defines the tag serializer
    """
    class Meta:
        model = Tag
        fields = ('tag',)

        def to_representation(self, obj):
            return obj.tag
