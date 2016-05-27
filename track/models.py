from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class URLAccount(models.Model):
	owner = models.ForeignKey(User)
	domain = models.URLField()
	_client_secret_md = models.TextField(null=True)
	_client_key_md = models.TextField(null=True)
	days_tracking_available = models.IntegerField(default=1)
	active = models.BooleanField(default=True)

	def get_client_key_md(self):
		import base64
		return base64.decodestring(self._client_key_md)

	def set_client_key_md(self, value):
		import base64
		self._client_key_md = base64.encodestring(value)

	def get_client_secret_md(self):
		import base64
		return base64.decodestring(self._client_secret_md)

	def set_client_secret_md(self, value):
		import base64
		self._client_secret_md = base64.encodestring(value)

	client_secret_md = property(get_client_secret_md, set_client_secret_md)
	client_key_md = property(get_client_key_md, set_client_key_md)



class Visitor(models.Model):
	datetime = models.DateTimeField(auto_now_add=True)
	id_generated_or_email = models.CharField(max_length=200, unique=True)
	email_organic_lead = models.CharField(max_length=125, null=True)
	date_update = models.DateTimeField(auto_now=True)

class VisitorTrack(models.Model):
	visitor = models.ForeignKey(Visitor)
	url_visited = models.CharField(max_length=100,db_index=True)
	time_remained_seconds = models.CharField(max_length=150)
	datetime = models.DateTimeField(auto_now_add=True)
	campaign = models.CharField(max_length=10, null=True)
	campaign_key = models.CharField(max_length=250, null=True, db_index=True)


class ConnectionURL(models.Model):
	url = models.TextField()
	user = models.CharField(max_length=100)
	kennwort = models.TextField()
	host = models.CharField(max_length=100)
	db = models.CharField(max_length=100)
	host1 = models.CharField(max_length=100)
	user_host = models.CharField(max_length=100)
	kennwort_host = models.TextField()


	def get_kennwort(self):
		import base64
		return base64.decodestring(self.kennwort)

	def set_kennwort(self, value):
		import base64
		self.kennwort = base64.encodestring(value)

	password = property(get_kennwort, set_kennwort)

	def get_kennwort_host(self):
		import base64
		return base64.decodestring(self.kennwort_host)

	def set_kennwort_host(self, value):
		import base64
		self.kennwort_host = base64.encodestring(value)

	password_host = property(get_kennwort_host, set_kennwort_host)