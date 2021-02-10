from rest_framework import serializers


class FollowUserSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=50, required=True, help_text="User Name")
    follow_user = serializers.CharField(max_length=50, required=True, help_text="Following User Name")
