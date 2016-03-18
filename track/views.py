from django.shortcuts import render
from django.http import JsonResponse
from track.models import Visitor,VisitorTrack
import uuid
# Create your views here.

def generate_unique_id(email=None):
	if email:
		try:
			return Visitor.objects.get(id_generated_or_email=email)
		except:
			return Visitor.objects.create(id_generated_or_email=email)
	else:
		try:
			return Visitor.objects.create(id_generated_or_email=uuid.uuid1())
		except:
			return generate_unique_id()


def generate_id(request):
	visitor = generate_unique_id(request.GET.get('email'))
	return JsonResponse({'id': visitor.id_generated_or_email})

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
	return JsonResponse({'cool': 'cool'})

