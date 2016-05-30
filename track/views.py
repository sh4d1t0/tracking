# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from track.models import Visitor,VisitorTrack, ConnectionURL, URLAccount, MappingVisitorData
import uuid, json
from django.views.decorators.csrf import csrf_exempt 
from track.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def generate_unique_id(email=None):
	if email:
		try:
			return Visitor.objects.get(id_generated_or_email=email)
		except:
			return Visitor.objects.create(id_generated_or_email=email)
	else:
		try:
			return Visitor.objects.create(id_generated_or_email=uuid.uuid1().get_hex())
		except:
			return generate_unique_id()

def get_miliseconds(days=1):
	import time
	ms = time.time()*1000.0
	return (86400000*days) + ms

def generate_id(request):
	visitor = generate_unique_id(request.GET.get('email'))
	campaign_name = ""
	if request.GET.get('c'):
		referer = request.META.get('HTTP_REFERER')
		origin = request.META.get('HTTP_ORIGIN')
		url = request.GET.get('host')
		campaign_name = get_campaign_name(url, request.GET.get('c'))
	url_account = URLAccount.objects.get(domain__contains=request.GET.get('host'))
	ends = get_miliseconds(url_account.days_tracking_available)	
	response = HttpResponse(json.dumps({'id': visitor.id_generated_or_email, 'c': campaign_name, 'ends': ends, 'c_key': request.GET.get('c', "")}), content_type='application/json')
	response['Access-Control-Allow-Origin'] = "*"
	return response

def match_email_organic_lead(request):
	organic_lead = request.GET.get('organic_lead')
	organic_lead_object = Visitor.objects.get(id_generated_or_email=organic_lead)
	values = request.GET.get('data', {})
	if type(values) != dict:
		if type(values) in (unicode, str):
			values = eval(values)
		else:
			return HttpResponse({'error': 'error'})
	keys = values.keys()
	mapping_data_visitor_data = MappingVisitorData.objects.filter(name_field__in=keys, active=True)
	if mapping_data_visitor_data.count():
		for mapp in mapping_data_visitor_data:
			setattr(organic_lead_object, mapp.name_field_table, values[mapp.name_field])
		organic_lead_object.save()
	return HttpResponse({'ok': 'ok'})


def get_campaign_name(url, campaign):
	from sshtunnel import SSHTunnelForwarder
	obj_url = ConnectionURL.objects.get(url__contains=url)
	import MySQLdb as mdb
	name = None
	with SSHTunnelForwarder(
         (obj_url.host1, 22),
         ssh_password=obj_url.password_host,
         ssh_username=obj_url.user_host,
         remote_bind_address=('127.0.0.1', 3306)) as server:

	    	con = None
	    	con = mdb.connect(host=obj_url.host, user=obj_url.user, passwd=obj_url.password, db=obj_url.db, port=server.local_bind_port)
	    	cur = con.cursor()
	    	cur.execute("SELECT name FROM campaigns WHERE id=%s LIMIT 1", (campaign, ))
	    	rowcount =  cur.rowcount
	    	if rowcount == 1:
	    		name = cur.fetchone()[0]
	return name
	

def test_1(request):
	return render(request, 'track/test1.html', locals())

def test_2(request):
	return render(request, 'track/test2.html', locals())

def save_data(request):
	page = request.GET.get('page')
	time = request.GET.get('time')
	campaign = request.GET.get('c')
	campaign_key = request.GET.get('c_key')
	assigned_id = request.GET.get('id')
	visitor = Visitor.objects.get(id_generated_or_email=assigned_id)
	vt = VisitorTrack.objects.create(visitor=visitor, url_visited=page, time_remained_seconds=time, campaign=campaign, campaign_key=campaign_key)
	response = HttpResponse(json.dumps({'cool': 'cool'}), content_type='application/json')
	response['Access-Control-Allow-Origin'] = "*"
	return response


def login_view(request):

	if request.user.is_authenticated():
		return HttpResponseRedirect('/report/')
	if request.method == "GET":
		form = LoginForm()
	else:
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/report/')
				else:
					form.add_error("username", u"Este usuario no esta activo")
			else:
				form.add_error("username", u"Por favor compruebe el usuario y contraseñas")
	return render(request, 'track/login.html', locals())

@login_required
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')
