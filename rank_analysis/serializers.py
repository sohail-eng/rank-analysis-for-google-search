from rest_framework import serializers


class SearchRequestSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    invites = serializers.ListField(required=True)


class SearchResponseSerializer(serializers.Serializer):
    task_id = serializers.UUIDField()


class TaskResultResponseSerializer(serializers.Serializer):
    task_id = serializers.UUIDField()
    status = serializers.CharField()
    result = serializers.JSONField()
