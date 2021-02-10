from rest_framework import serializers

class UserPostRequestSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=50, required=True, help_text="User Name")
    password = serializers.CharField(max_length=50, required=True, help_text="Password")
    email = serializers.EmailField(help_text="Email Id")
    first_name = serializers.CharField(max_length=50, help_text="First Name")
    last_name = serializers.CharField(max_length=50, help_text="Last Name")