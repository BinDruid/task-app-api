from rest_framework import serializers

from apps.accounts.serializers import UserSerializer

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "owner",
            "created_at",
            "updated_at",
            "finished_at",
            "is_finished",
        ]

    def to_representation(self, instance):
        instance_dict = super().to_representation(instance)
        instance_dict["owner"] = instance_dict["owner"]["username"]
        if instance_dict["is_finished"]:
            del instance_dict["is_finished"]
        else:
            del instance_dict["finished_at"]
        return instance_dict
