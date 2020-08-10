# fake commit1
from rest_framework import serializers

from todo.models import Task, SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('id', 'title', 'description')

class TaskSerializer(serializers.ModelSerializer):

    sub_tasks = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'state', 'due_date', 'sub_tasks')

    def get_sub_tasks(self, obj):
        subtasks = obj.subtasks.all()
        serializer = SubTaskSerializer(subtasks, many=True)
        return serializer.data
