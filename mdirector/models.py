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
	total_sent = models.IntegerField()
	bounces = models.IntegerField()
	bounces_percentage = models.DecimalField(decimal_places=2, max_digits=14)
	clicks = models.IntegerField()
	clicks_percentage = models.DecimalField(decimal_places=2, max_digits=14)
	deliveries = models.IntegerField()
	deliveries_percentage = models.DecimalField(decimal_places=2, max_digits=14)
	openings = models.IntegerField()
	openings_total = models.IntegerField()
	openings_percentage = models.DecimalField(decimal_places=2, max_digits=14)
	openings_percentage_total = models.DecimalField(decimal_places=2, max_digits=14)
	conversion_rate = models.DecimalField(decimal_places=2, max_digits=14)

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
		return "%.2f" % calculate_percentage(self.deliveries, self.clicks)


	def get_openings_percentage(self):
		from report.views import calculate_percentage
		return "%.2f" % calculate_percentage(self.deliveries, self.openings)


class StatsDelivery(models.Model):
	campaign = models.ForeignKey(Campaign)
	email = models.CharField(max_length=100)
	date = models.DateTimeField()
	url = models.CharField(max_length=200, null=True)
	reason = models.TextField(null=True)
	type_stats = models.CharField(max_length=20)



class DataUpdate(models.Model):
	url_acccount = models.ForeignKey('track.URLAccount')
	last_update = models.IntegerField()
	data_type = models.CharField(max_length=20)

	class Meta:
		unique_together = ('url_acccount', 'last_update', 'data_type')