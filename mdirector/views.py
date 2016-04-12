from django.shortcuts import render

from .models import Campaign, Delivery
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

    de.total_sent = int(de.deliveries) + int(de.bounces)
    de.bounces_percentage = calculate_percentage(de.total_sent, de.bounces)
    de.clicks_percentage =  calculate_percentage(de.deliveries, de.clicks)
    de.deliveries_percentage = calculate_percentage(de.total_sent, de.deliveries)
    de.openings_percentage = calculate_percentage(de.deliveries, de.openings)
    try:
      de.conversion_rate = (float(de.clicks*100) / de.openings)
    except:
      de.conversion_rate = 0
    de.save()
