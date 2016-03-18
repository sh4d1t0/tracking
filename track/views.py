from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from track.models import Visitor,VisitorTrack
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
	response = HttpResponse(json.dumps({'id': visitor.id_generated_or_email}), content_type='application/json')
	response['Access-Control-Allow-Origin'] = "*"
	return response

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

