from rest_framework import serializers

from user.serializers import UserSerializer
from webcam import models


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the webcam comment object"""
    user_added = UserSerializer(read_only=True)
    date_added = serializers.DateField(read_only=True, format='%d %B %Y')

    class Meta:
        model = models.Comment
        fields = (
            'user_added',
            'content',
            'date_added',
            'webcam',
        )
        write_only_fields = (
            'webcam',
        )


class WebcamSerializer(serializers.ModelSerializer):
    """Serializer for the webcam object"""
    date_added = serializers.DateField(read_only=True, format='%d %B %Y')
    user_added = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True, source='comment_set')

    class Meta:
        model = models.Webcam
        fields = (
            'name',
            'description',
            'url',
            'thumbnail_url',
            'latitude',
            'longitude',
            'category',
            'country',
            'date_added',
            'user_added',
            'comments',
        )


class WebcamLocationFilterSerializer(serializers.Serializer):
    user_lat = serializers.FloatField(required=False)
    user_lon = serializers.FloatField(required=False)
    max_radius = serializers.IntegerField(required=False)
