from rest_framework import serializers

class UserGetRequestSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=50, required=True, help_text="User Name")