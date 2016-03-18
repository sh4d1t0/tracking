from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class URLAccount(models.Model):
	owner = models.ForeignKey(User)
	domain = models.URLField()


class Visitor(models.Model):
	datetime = models.DateTimeField(auto_now_add=True)
	id_generated_or_email = models.CharField(max_length=200, unique=True)

class VisitorTrack(models.Model):
	visitor = models.ForeignKey(Visitor)
	url_visited = models.TextField()
	time_remained_seconds = models.CharField(max_length=150)