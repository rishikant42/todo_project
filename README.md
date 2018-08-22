### ToDo list application

A simple todo list application written in Python with django web framework.

##### Install instruction
- $ git clone https://github.com/rishikant42/todo_project

- $ cd todo_project

##### Create virtual env & Install dependencies:
- $ virtualenv env

- $ source env/bin/activate

- $ pip install -r requirements.txt

##### DB setup
- Create mysql Db `mysql> create database todo;`

- Update db-conf in ./todo_project/settings.py. You may need to save db-username & db-password in ~/.bashrc (or ~/.bash_profile). 

- Apply migration to DB ` $ python manage.py migrate`

##### Run test cases

- $ python manage.py test

##### Load test data in DB & run runserver
- $ python manage.py loaddata testdata.json

- $ python manage.py runserver 8787

### Examples

##### List all task

```
$ curl http://127.0.0.1:8787/tasks/ | json_pp
[
   {
      "state" : 1,
      "due_date" : "2018-08-20",
      "title" : "Task-this-week-first-day",
      "id" : 3,
      "sub_tasks" : [
         {
            "title" : "subtask4",
            "description" : "Description4",
            "id" : 4
         }
      ],
      "description" : "Description-this-week-first"
   },
   {
      "sub_tasks" : [
         {
            "description" : "Description3",
            "id" : 3,
            "title" : "subtask3"
         }
      ],
      "id" : 2,
      "description" : "Description-yesterday",
      "due_date" : "2018-08-21",
      "state" : 1,
      "title" : "Task-yesterday"
   },
   {
      "state" : 1,
      "due_date" : "2018-08-22",
      "title" : "Task-today",
      "id" : 1,
      "sub_tasks" : [
         {
            "id" : 1,
            "description" : "Description1",
            "title" : "subtask1"
         },
         {
            "id" : 2,
            "description" : "Description2",
            "title" : "Subtask2"
         }
      ],
      "description" : "Description-today"
   },
   {
      "title" : "Task-this-week-last-day",
      "due_date" : "2018-08-26",
      "state" : 1,
      "description" : "Description-this-week-last",
      "sub_tasks" : [],
      "id" : 4
   },
   {
      "title" : "Task-next-week-first-day",
      "state" : 1,
      "due_date" : "2018-08-27",
      "description" : "Description-next-week-first",
      "id" : 5,
      "sub_tasks" : []
   },
   {
      "state" : 1,
      "due_date" : "2018-09-02",
      "title" : "Task-next-week-last-day",
      "id" : 6,
      "sub_tasks" : [],
      "description" : "Description-next-week-last"
   }
]
```

### Create new task

```
$ curl -X POST -H "Content-Type: application/json" -d '{"title": "title-new", "description": "description-new", "due_date":"2018-08-14", "sub_tasks": [{"title": "subTask-3"}, {"title": "subTask-2"} ] }' http://127.0.0.1:8787/tasks/ | json_pp

{
   "title" : "title-new",
   "state" : 1,
   "description" : "description-new",
   "sub_tasks" : [
      {
         "description" : null,
         "title" : "subTask-3",
         "id" : 9
      },
      {
         "title" : "subTask-2",
         "description" : null,
         "id" : 10
      }
   ],
   "id" : 18,
   "due_date" : "2018-08-14"
}
```

### Filters (due-date=this-week)

```
$ curl  http://127.0.0.1:8787/tasks/?due-date=this-week | json_pp

[
   {
      "id" : 3,
      "state" : 1,
      "description" : "Description-this-week-first",
      "due_date" : "2018-08-20",
      "sub_tasks" : [
         {
            "description" : "Description4",
            "id" : 4,
            "title" : "subtask4"
         }
      ],
      "title" : "Task-this-week-first-day"
   },
   {
      "state" : 1,
      "due_date" : "2018-08-21",
      "description" : "Description-yesterday",
      "id" : 2,
      "title" : "Task-yesterday",
      "sub_tasks" : [
         {
            "title" : "subtask3",
            "description" : "Description3",
            "id" : 3
         }
      ]
   },
   {
      "title" : "Task-today",
      "sub_tasks" : [
         {
            "id" : 1,
            "description" : "Description1",
            "title" : "subtask1"
         },
         {
            "id" : 2,
            "description" : "Description2",
            "title" : "Subtask2"
         }
      ],
      "state" : 1,
      "due_date" : "2018-08-22",
      "description" : "Description-today",
      "id" : 1
   },
   {
      "title" : "Task-this-week-last-day",
      "sub_tasks" : [],
      "state" : 1,
      "description" : "Description-this-week-last",
      "due_date" : "2018-08-26",
      "id" : 4
   }
]

```

### Filter: due-date=next-week and state=pending
```
$ curl 'http://127.0.0.1:8787/tasks/?due-date=next-week&state=pending' | json_pp

[
   {
      "due_date" : "2018-08-27",
      "sub_tasks" : [],
      "state" : 1,
      "description" : "Description-next-week-first",
      "id" : 5,
      "title" : "Task-next-week-first-day"
   },
   {
      "description" : "Description-next-week-last",
      "id" : 6,
      "title" : "Task-next-week-last-day",
      "due_date" : "2018-09-02",
      "state" : 1,
      "sub_tasks" : []
   }
]

```

### Filter: due-date=today & state=pending

```
$ curl 'http://127.0.0.1:8787/tasks/?due-date=today&state=pending' | json_pp

[
   {
      "due_date" : "2018-08-22",
      "sub_tasks" : [
         {
            "id" : 1,
            "description" : "Description1",
            "title" : "subtask1"
         },
         {
            "title" : "Subtask2",
            "id" : 2,
            "description" : "Description2"
         }
      ],
      "title" : "Task-today",
      "id" : 1,
      "state" : 1,
      "description" : "Description-today"
   }
]

```

### ToDO
- Need to create frontend for APIs
