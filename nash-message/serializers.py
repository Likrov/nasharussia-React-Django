from django.conf import settings
from rest_framework import serializers
from profiles.serializers import PublicProfileSerializer
from .models import Nash_message

MAX_NASH_MESSAGE_LENGTH = settings.MAX_NASH_MESSAGE_LENGTH
NASH_MESSAGE_ACTION_OPTIONS = settings.NASH_MESSAGE_ACTION_OPTIONS

class Nash_messageActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip() # "Like " -> "like"
        if not value in NASH_MESSAGE_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for nash-message")
        return value


class Nash_messageCreateSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True) # serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Nash_message
        fields = ['user', 'id', 'content', 'likes', 'timestamp']
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    def validate_content(self, value):
        if len(value) > MAX_NASH_MESSAGE_LENGTH:
            raise serializers.ValidationError("This nash_message is too long")
        return value

    # def get_user(self, obj):
    #     return obj.user.id


class Nash_messageSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    parent = Nash_messageCreateSerializer(read_only=True)
    class Meta:
        model = Nash_message
        fields = [
                'user', 
                'id', 
                'content',
                'likes',
                'is_renash',
                'parent',
                'timestamp']

    def get_likes(self, obj):
        return obj.likes.count()
