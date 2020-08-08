# fake commit
from django.conf.urls import url

from views import TaskList, TaskDetail, Slack

urlpatterns = [
    url(r'^tasks/?$', TaskList.as_view(), name='task_list_api'),
    url(r'^slack/$', Slack.as_view(), name='task_list_api'),
    url(r'^tasks/(?P<pk>[0-9]+)/$', TaskDetail.as_view(), name='task_detail_api'),
]
