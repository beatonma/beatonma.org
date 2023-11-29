from rest_framework import serializers


class ApiSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="api_id")
