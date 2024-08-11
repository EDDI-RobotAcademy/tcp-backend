from rest_framework import serializers

class GoogleOauthUrlSerializer(serializers.Serializer):
    url = serializers.URLField()