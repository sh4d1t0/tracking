from django.shortcuts import render

from .models import Campaign, Delivery, StatsDelivery
from .mdirectorapi import MdirectorAPI

# Create your views here.


def update_campaigns(urlaccount):
	md = MdirectorAPI(urlaccount.client_key_md, urlaccount.client_secret_md)
	campagins = md.Campaigns.get_campaigns()
	info = campagins['data']
	for campaign in info:
		if not "test" in campaign['campaignName'].lower():
			c = Campaign.objects.get_or_create(campaign_id=campaign['id'], owner=urlaccount, defaults={
				'campaign_id': campaign['id'],
				'owner': urlaccount,
				'campaign_name': campaign['campaignName']
				})

def update_delivery(urlaccount):
  from report.views import calculate_percentage
  md = MdirectorAPI(urlaccount.client_key_md, urlaccount.client_secret_md)
  deliveries = md.Deliveries.get_delivery()
  info = deliveries['data']['data']
  for delivery in info:
    try:
      de = Delivery.objects.get(envid=delivery['envId'], campaign__owner=urlaccount)
    except:
      de = Delivery()
      de.campaign = Campaign.objects.get(owner=urlaccount,campaign_id=delivery['camId'] )   
      de.envid = delivery['envId']
      de.name = delivery['name']
    stats = md.Stats.get_stats(int(delivery['envId']))
    
    de.subject = delivery['subject']
    de.bounces = int(delivery['bounces'])
    de.clicks = int(stats['clicks']['net'])
    de.deliveries = int(delivery['deliveries'])
    de.openings = int(stats['opens']['net'])
    de.openings_total = int(stats['opens']['total'])

    de.total_sent = int(de.deliveries) + int(de.bounces)
    de.bounces_percentage = calculate_percentage(de.total_sent, de.bounces)
    de.clicks_percentage =  calculate_percentage(de.deliveries, de.clicks)
    de.deliveries_percentage = calculate_percentage(de.total_sent, de.deliveries)
    de.openings_percentage = calculate_percentage(de.deliveries, de.openings)
    de.openings_percentage_total = calculate_percentage(de.deliveries, de.openings_total)
    try:
      de.conversion_rate = (float(de.clicks*100) / de.openings)
    except:
      de.conversion_rate = 0
    de.save()




def update_statsdelivery(urlaccount):
  from report.views import calculate_percentage
  from datetime import datetime
  md = MdirectorAPI(urlaccount.client_key_md, urlaccount.client_secret_md)
  deliveries = Delivery.objects.filter(campaign__owner=urlaccount)
  stats = md.Stats
  for delivery in deliveries:
    opens = stats.get_stats(delivery.envid, data="opens")
    clicks = stats.get_stats(delivery.envid, data="clicks")
    failures = stats.get_stats(delivery.envid, data="failures")
    for _open in opens['data']:
      campaign = Campaign.objects.get(campaign_name=_open['campaign'], owner=urlaccount)
      date_object = datetime.strptime(_open['date'], '%Y-%m-%d %H:%M:%S')
      StatsDelivery.objects.create(campaign=campaign, email=_open['email'], date=date_object, type_stats="opens")

    for _clicks in clicks['data']:
      campaign = Campaign.objects.get(campaign_name=_clicks['campaign'], owner=urlaccount)
      date_object = datetime.strptime(_clicks['date'], '%Y-%m-%d %H:%M:%S')
      StatsDelivery.objects.create(campaign=campaign, email=_clicks['email'], date=date_object, url=_clicks['url'], type_stats="clicks")

    for _failure in failures['data']:
      campaign = Campaign.objects.get(campaign_name=_failure['campaign'], owner=urlaccount)
      date_object = datetime.strptime(_failure['date'], '%Y-%m-%d %H:%M:%S')
      StatsDelivery.objects.create(campaign=campaign, email=_failure['email'], date=date_object, reason=_failure['reason'], type_stats="failures")

