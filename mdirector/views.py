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
		
		de.subject = delivery['subject']
		de.bounces = delivery['bounces']
		de.clicks = delivery['clicks']
		de.deliveries = delivery['deliveries']
		de.openings = delivery['openings']
		de.save()

