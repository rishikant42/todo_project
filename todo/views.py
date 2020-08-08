# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, date, timedelta

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import View

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from todo.models import Task, SubTask
from todo.serializers import TaskSerializer
from todo.celery_tasks import task_alert


class Slack(APIView):
    def post(self, request):
        response = {
            'challenge': request.data.get('challenge')
        }
        return Response(response)


class TaskList(APIView):
    """
    HTTP_ALLOWED_METHODS: GET, POST

    METHOD GET
        Return list of existing tasks

    METHOD POST:
        Create a new task in table
    """
    def get_filter_keys(self):
        filter_keys = {}

        title = self.request.query_params.get('title', None)
        due_date = self.request.query_params.get('due-date', None)
        state = self.request.query_params.get('state', None)

        if title:
            filter_keys['title__icontains'] = title

        if due_date:
            due_date = due_date.lower()
            today_date = date.today()

            if due_date == 'this-week':
                # go back to monday
                this_week_first_day = today_date - timedelta(days=today_date.weekday())

                # monday to upcoming sunday
                this_week_last_day = this_week_first_day + timedelta(days=6)

                filter_keys['due_date__range'] = [this_week_first_day, this_week_last_day]
                # filter_keys['state'] = Task.PENDING

            elif due_date == 'next-week':
                # jump to next monday
                next_week_first_day = today_date + timedelta(days=7-today_date.weekday())

                # next monday to next upcoming sunday
                next_week_last_day = next_week_first_day + timedelta(days=6)

                filter_keys['due_date__range'] = [next_week_first_day, next_week_last_day]

            elif due_date == 'overdue':
                filter_keys['due_date__lt'] = today_date

            elif due_date == 'today':
                filter_keys['due_date'] = today_date

            else:
                pass

        if state:
            state = state.lower()

            if state == 'pending':
                filter_keys['state'] = Task.PENDING

            elif state == 'completed':
                filter_keys['state'] = Task.COMPLETED

            else:
                pass

        return filter_keys


    def get(self, request):
        filter_keys = self.get_filter_keys()

        tasks = Task.objects.filter(**filter_keys)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        sub_tasks = request.data.pop('sub_tasks', None)
        alert_hours = request.data.pop('alert_hours', None)

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            if sub_tasks:
                for sub_task in sub_tasks:
                    SubTask.objects.create(task=serializer.instance, **sub_task)

            due_date = serializer.instance.due_date

            # task alert
            if due_date and alert_hours:
                task_id = serializer.instance.id
                task_title = serializer.instance.title

                alert_time = due_date - timedelta(hours=alert_hours)

                task_alert.apply_async((task_id, task_title), eta=alert_time)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    """
    HTTP_ALLOWED_METHODS: GET, PATCH, DELETE

    METHOD GET:
        Return detail of specifed task instance

    METHOD PATCH:
        Update & return specified task instance

    METHOD DELETE:
        Delete specified task instance
    """
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def patch(self, request, pk):
        task = self.get_object(pk)
        data = {
            'title': request.data.get('title', task.title),
            'description': request.data.get('description', task.description),
            'state': request.data.get('state', task.state),
            'due_date': request.data.get('due_date', task.due_date),
        }

        serializer = TaskSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
