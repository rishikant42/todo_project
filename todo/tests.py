# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date, timedelta
import json

from django.test import TestCase, Client
from django.urls import reverse

from todo.models import Task


class TaskApiTest(TestCase):
    def setUp(self):
        self.client = Client()

        Task.objects.create(title="title1", description="description1")
        Task.objects.create(title="title2", description="description2")

    def test_get_task_list(self):
        response = self.client.get(reverse('task_list_api'))
        data = response.json()
        status = response.status_code
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 2)

    def test_create_task(self):
        data = {"title": "title3", "description": "description3", "due_date":"2018-08-14"}
        json_data = json.dumps(data)
        response = self.client.post(reverse('task_list_api'), json_data, content_type="application/json")
        status = response.status_code
        self.assertEqual(status, 201)


class TaskApiFiltersTest(TestCase):
    def setUp(self):
        self.client = Client()

        today_date = date.today()
        yesterday_date = today_date - timedelta(1)

        this_week_first_day = today_date - timedelta(days=today_date.weekday())
        this_week_last_day = this_week_first_day + timedelta(6)

        next_week_first_day = today_date + timedelta(days=7-today_date.weekday())
        next_week_last_day = next_week_first_day + timedelta(days=6)

        Task.objects.create(title="Task-today", due_date=today_date)
        Task.objects.create(title="Task-yesterday", due_date=yesterday_date)

        Task.objects.create(title="Task-this-week-first-day", due_date=this_week_first_day)
        Task.objects.create(title="Task-this-week-last-day", due_date=this_week_last_day)

        Task.objects.create(title="Task-next-week-first-day", due_date=next_week_first_day)
        Task.objects.create(title="Task-next-week-last-day", due_date=next_week_last_day)

    def test_filter_by_today(self):
        response = self.client.get(reverse('task_list_api') + '/?due-date=today')
        data = response.json()
        title = data[0].get('title')
        status = response.status_code

        self.assertEqual(status, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(title, "Task-today")

    def test_filter_by_this_week(self):
        response = self.client.get(reverse('task_list_api') + '/?due-date=this-week')
        data = response.json()
        titles = [i.get('title') for i in data]
        status = response.status_code

        self.assertEqual(status, 200)
        self.assertIn("Task-this-week-first-day", titles)
        self.assertIn("Task-this-week-last-day", titles)

    def test_filter_by_next_week(self):
        response = self.client.get(reverse('task_list_api') + '/?due-date=next-week')
        data = response.json()
        titles = [i.get('title') for i in data]
        status = response.status_code

        self.assertEqual(status, 200)
        self.assertEqual(len(data), 2)
        self.assertIn("Task-next-week-first-day", titles)
        self.assertIn("Task-next-week-last-day", titles)

    def test_filter_by_overdue(self):
        response = self.client.get(reverse('task_list_api') + '/?due-date=overdue')
        data = response.json()
        titles = [i.get('title') for i in data]
        status = response.status_code

        self.assertEqual(status, 200)
        self.assertIn("Task-yesterday", titles)
