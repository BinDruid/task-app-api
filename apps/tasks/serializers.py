from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "created_at",
        ]


class TaskDetailSerializer(TaskSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = TaskSerializer.Meta.fields + [
            "owner",
            "updated_at",
            "finished_at",
            "is_finished",
        ]

    def to_representation(self, instance):
        instance_dict = super().to_representation(instance)
        if instance_dict["is_finished"]:
            del instance_dict["is_finished"]
        else:
            del instance_dict["finished_at"]
        return instance_dict
