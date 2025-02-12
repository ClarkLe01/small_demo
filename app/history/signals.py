from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TaskHistory
from notification.models import Notification


@receiver(post_save, sender=TaskHistory)
def notify_task_update(sender, instance, created, **kwargs):
    if instance.object == "Task":
        message = "{0} {1} in Project {2} (ID: {3}) ".format(instance.action, instance.task.title,
                                                             instance.task.project.name, instance.task.project.id)
    elif instance.object == "Comment":
        message = "{0} {1} in {2}".format(instance.action, instance.object, instance.task.title)
    else:
        message = "Something went wrong"

    participants = [user for user in instance.task.project.collaborators.all()]
    participants.append(instance.task.project.created_by)
    for user in participants:
        if user != instance.user:
            Notification.objects.create(message=message, user=user, changed_by=instance.user)
