from rest_framework import serializers


class TweetGetRequestSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=50, required=True, help_text="User Name")
    tweet = serializers.CharField(max_length=280, required=False, help_text="Tweet")
    id = serializers.IntegerField(required=False, help_text="Tweet Id")
