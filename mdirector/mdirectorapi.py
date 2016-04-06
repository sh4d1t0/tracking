# -*- coding: utf-8 -*-

#PPO
#client_key  = "39323"
#client_secret = "1db0d54f27545a2269a5"

from requests_oauthlib import OAuth1
import requests, urllib


class Connection(object):
	
	def connect(self):
		if not self.connection:
			self.connection = OAuth1(self.ck, client_secret=self.cs)		
		return self.connection

	def send_request(self, method, url, data={}):
		method = method.lower()
		if method == "get":
			req = self.send_get(url, data)
		elif method == "post":
			req = self.send_post(url, data)
		elif method == "put":
			req = self.send_put(url, data)
		elif method == "delete":
			req = self.send_delete(url, data)
		return req.json()

	def send_get(self, url, data={}):
		if data:
			url = url + "?"+ urllib.urlencode(data)
		return requests.get(url, auth=self.connect())

	def send_post(self, url, data={}):
		return requests.post(url, auth=self.connect(), data=data)

	def send_put(self, url, data={}):
		return requests.put(url, auth=self.connect(), data=data)

	def send_delete(self, url, data={}):
		return requests.delete(url, auth=self.connect(), data=data)

	def __init__(self, ck, cs):
		self.ck = ck
		self.cs = cs
		self.connection = None
		self.connect()


class CampaignsAPI(Connection):
	
	def get_campaigns(self, _id=""):
		data = {}
		if _id:
			data = {'id': _id}
		return self.send_request("GET", self.base_url, data=data)
	
	def __init__(self, ck, cs):
		self.base_url = "http://www.mdirector.com/api_campaign"
		super(CampaignsAPI, self).__init__(ck, cs)


class DeliveriesAPI(Connection):
	
	def get_delivery(self, envId=""):
		data = {}
		if envId:
			data = {'envId': envId}
		return self.send_request("GET", self.base_url, data=data)
	
	def __init__(self, ck, cs):
		self.base_url = "http://www.mdirector.com/api_delivery"
		super(DeliveriesAPI, self).__init__(ck, cs)

class StatsAPI(Connection):
	def get_stats(self, envid):
		return self.send_request("GET", self.base_url, data={'envid': envid})
	
	def __init__(self, ck, cs):
		self.base_url = "http://www.mdirector.com/api_stats"
		super(StatsAPI, self).__init__(ck, cs)


class MdirectorAPI(object):

	def __init__(self, ck, cs):
		self.ck = ck
		self.cs = cs	
	
	def get_stats(self):
		return StatsAPI(self.ck, self.cs)

	Stats = property(get_stats)

	def get_deliveries(self):
		return DeliveriesAPI(self.ck, self.cs)

	Deliveries = property(get_deliveries)

	def get_campaigns(self):
		return CampaignsAPI(self.ck, self.cs)

	Campaigns = property(get_campaigns)
