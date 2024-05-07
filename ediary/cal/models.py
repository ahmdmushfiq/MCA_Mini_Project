from datetime import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Event(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title}</a>'
    
class Entry(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

# class Entries(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     text = models.TextField()
#     date_posted = models.DateTimeField(default=timezone.now)