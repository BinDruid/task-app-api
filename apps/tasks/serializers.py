from rest_framework import serializers

from .models import Tag, Task


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "title", "description"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Task.objects.create(owner=user, **validated_data)


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
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = TaskSerializer.Meta.fields + ["tags", "updated_at", "finished_at", "is_finished"]

    def create(self, validated_data):
        user = self.context["request"].user
        tags = validated_data.pop("tags", [])
        new_task = Task.objects.create(owner=user, **validated_data)
        for tag_context in tags:
            new_tag, created = Tag.objects.get_or_create(owner=user, **tag_context)
            new_task.add(new_tag)
        return new_task

    def to_representation(self, instance):
        instance_dict = super().to_representation(instance)
        if instance_dict["is_finished"]:
            del instance_dict["is_finished"]
        else:
            del instance_dict["finished_at"]
        return instance_dict
