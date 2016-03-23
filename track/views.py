from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from track.models import Visitor,VisitorTrack, ConnectionURL
import uuid, json
from django.views.decorators.csrf import csrf_exempt 

# Create your views here.



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

def generate_id(request):
	visitor = generate_unique_id(request.GET.get('email'))
	campaign_name = ""
	print request.META.get('HTTP_ORIGIN'), "WII"
	if request.GET.get('c'):
		campaign_name = get_campaign_name(request.META.get('HTTP_ORIGIN'), request.GET.get('c'))
	response = HttpResponse(json.dumps({'id': visitor.id_generated_or_email, 'c': campaign_name}), content_type='application/json')
	response['Access-Control-Allow-Origin'] = "*"
	return response

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
	assigned_id = request.GET.get('id')
	visitor = Visitor.objects.get(id_generated_or_email=assigned_id)
	vt = VisitorTrack.objects.create(visitor=visitor, url_visited=page, time_remained_seconds=time)
	response = HttpResponse(json.dumps({'cool': 'cool'}), content_type='application/json')
	response['Access-Control-Allow-Origin'] = "*"
	return response

