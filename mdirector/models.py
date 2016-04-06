from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Campaign(models.Model):
	owner = models.ForeignKey('track.URLAccount')
	campaign_name = models.CharField(max_length=100)
	campaign_id = models.CharField(max_length=10)

class Delivery(models.Model):
	campaign = models.ForeignKey('Campaign')
	envid = models.IntegerField()
	name = models.CharField(max_length=100)
	subject = models.CharField(max_length=150)
	bounces = models.IntegerField()
	clicks = models.IntegerField()
	deliveries = models.IntegerField()
	openings = models.IntegerField()

	def cr(self):
		try:
			return "%.2f" % (float(self.clicks*100) / self.openings)
		except:
			return 0

	def get_total_sent(self):
		return self.bounces + self.deliveries

	def get_bounces_percentage(self):
		from report.views import calculate_percentage
		return "%.2f" % calculate_percentage(self.get_total_sent(), self.bounces)

	def get_deliveries_percentage(self):
		from report.views import calculate_percentage
		return "%.2f" % calculate_percentage(self.get_total_sent(), self.deliveries)

	def get_clicks_percentage(self):
		from report.views import calculate_percentage
		return "%.2f" % calculate_percentage(self.deliveries, self.bounces)


	def get_openings_percentage(self):
		from report.views import calculate_percentage
		return "%.2f" % calculate_percentage(self.deliveries, self.openings)
