from __future__ import unicode_literals

from datetime import date, timedelta

from django.db import models


class Task(models.Model):
    PENDING = 1
    COMPLETED = 2

    STATE_CHOICES = (
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    state = models.IntegerField(choices=STATE_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('due_date', )

    def __unicode__(self):
        return "{}".format(self.title)


class SubTask(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)

    def __unicode__(self):
        return "{}".format(self.title)

