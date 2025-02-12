from django.db import models
from simple_history.models import HistoricalRecords
from user.models import User
from ckeditor.fields import RichTextField
from project.models import Project


# Create your models here.
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    BACKLOG = 'backlog'
    TODO = 'todo'
    WORKING = 'working'
    DONE = 'done'
    STATUS_CHOICES = [(BACKLOG, 'backlog'), (TODO, 'todo'), (WORKING, 'working'), (DONE, 'done')]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=BACKLOG)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField()
    task_details = models.CharField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.project.name + ' - ' + self.title


class TaskComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    description = RichTextField()
    history = HistoricalRecords()

    def __str__(self):
        return self.task.title
