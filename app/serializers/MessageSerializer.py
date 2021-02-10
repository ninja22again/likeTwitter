from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    validation_errors = serializers.BooleanField(required=True, default=True)
    error_data = serializers.CharField(max_length=None, required=True)