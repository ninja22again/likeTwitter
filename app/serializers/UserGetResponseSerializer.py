from rest_framework import serializers

# from app.serializers.MessageSerializer import MessageSerializer


class UserGetResponseSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=50, required=True, help_text="User Name")
    email = serializers.EmailField(help_text="Email Id")
    first_name = serializers.CharField(max_length=50, help_text="First Name")
    last_name = serializers.CharField(max_length=50, help_text="Last Name")
    is_active = serializers.BooleanField(help_text="Is_active")
    created_at = serializers.DateTimeField(help_text="created at")
