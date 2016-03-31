# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db import connection
from django.db.models import Sum, Count
from track.models import VisitorTrack, URLAccount
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
import itertools


def get_months():
	meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
	"Septiembre", "Octubre", "Noviembre", "Diciembre"]
	return meses

def get_hours():
	return range(1, 25)

def get_month_name(month_number):
	return get_months()[int(month_number)-1]


@login_required
def report_monthly(request):
	url = request.GET.get('u')
	truncate_date = connection.ops.date_trunc_sql('month', 'datetime')
	qs = VisitorTrack.objects.filter(url_visited=url).extra({'month':truncate_date})
	report = qs.values('month').annotate(time=Sum('time_remained_seconds')).order_by('month')
	
	months = get_months()
	num_months = len(months)
	temp_list = [0,0,0,0,0,0,0,0,0,0,0,0]
	for mn in range(1, num_months):
		for r in report:
			if r['month'].month == mn:
				temp_list[mn-1] = r['time']
				break
	info_to_return = {'url': url, 'data': temp_list, 'months': get_months()}
	return JsonResponse(info_to_return, safe=False)

def get_number_days_month(year, month):
	from calendar import monthrange
	return monthrange(year, month)

@login_required
def report_monthly_view(request):
	url = request.GET.get('u')
	year = request.GET.get('y')
	if not url or not year:
		raise Http404
	truncate_date = connection.ops.date_trunc_sql('month', 'datetime')
	qs = VisitorTrack.objects.filter(url_visited=url, datetime__year=year).extra({'month':truncate_date})
	report = qs.values('month').annotate(time=Sum('time_remained_seconds')).order_by('month')
	
	months = get_months()
	num_months = len(months)
	temp_list = ['Tiempo visitado en segundos',0,0,0,0,0,0,0,0,0,0,0,0]
	for mn in range(1, num_months):
		for r in report:
			if r['month'].month == mn:
				temp_list[mn] = r['time']
				break
	info_to_return = {'url': url, 'data': temp_list, 'months': ['meses'] + get_months(), 'year': year}
	return render(request, 'report/url_monthly.html', locals())

@login_required
def report_days_view(request):
	url = request.GET.get('u')
	year = request.GET.get('y')
	m = request.GET.get('m')
	if not url or not year or not m:
		raise Http404
	truncate_date = connection.ops.date_trunc_sql('day', 'datetime')
	qs = VisitorTrack.objects.filter(url_visited=url, datetime__year=year, datetime__month=m).extra({'day':truncate_date})
	report = qs.values('day').order_by('datetime__day').annotate(time=Sum('time_remained_seconds')).order_by('day')
	number_days = get_number_days_month(int(year), int(m))
	temp_list = ['Tiempo visitado en segundos'] + ([0] * number_days[1])
	
	for dn in range(1, number_days[1]):
		for r in report:
			if r['day'].day == dn:
				temp_list[dn] = r['time']
				break
	info_to_return = {'url': url, 'data': temp_list, 'year': year, 'month': get_month_name(m), 'days': ['dias'] + range(1, number_days[1]+1)}
	return render(request, 'report/url_daily.html', locals())

@login_required
def report_year_view(request):
	url = request.GET.get('u')
	if not url:
		raise Http404
	truncate_date = connection.ops.date_trunc_sql('year', 'datetime')
	qs = VisitorTrack.objects.filter(url_visited=url).extra({'year':truncate_date})
	report = qs.values('year').annotate(time=Sum('time_remained_seconds')).order_by('year')
	temp_list = ['Tiempo visitado en segundos']
	years_list = ['years']
	for data in report:
		temp_list.append(data['time'])
		years_list.append(data['year'].year)
	info_to_return = {'url': url, 'data': temp_list, 'years': years_list}
	return render(request, 'report/url_year.html', locals())

def calculate_percentage(hundred, partial):
	return (partial*100.0)/hundred

@login_required
def report_url_domain(request):
	domain = request.GET.get('d')
	if not domain:
		raise Http404
	qs = VisitorTrack.objects.filter(url_visited__contains=domain)
	report = qs.values('url_visited').annotate(times=Count('url_visited')).order_by('times')
	total =  sum(map(lambda x: x['times'], report))
	percentages = ['porcentaje']
	urls = ['URL']
	temp = []
	for data in report:
		temp.append([str(data['url_visited']), calculate_percentage(total, data['times']) ])
	info_to_return = {'domain': domain, 'data': temp}
	return render(request, 'report/url_domain.html', locals())

@login_required
def report_url_day_view(request):
	url = request.GET.get('u')
	year = request.GET.get('y')
	m = request.GET.get('m')
	d = request.GET.get('d')
	if not url or not year or not m or not d:
		raise Http404
	truncate_date = connection.ops.date_trunc_sql('hour', 'datetime')
	qs = VisitorTrack.objects.filter(url_visited=url, datetime__year=year, datetime__month=m, datetime__day=d).extra({'hour':truncate_date})
	report = qs.values('hour').order_by('datetime__hour').annotate(time=Sum('time_remained_seconds')).order_by('hour')
	
	hours = get_hours()
	temp_list = ['Tiempo visitado en segundos'] + ([0] * 24)
	for dn in hours:
		for r in report:
			hour = r['hour'].hour
			if r['hour'].hour == 0:
				hour = 24
			if hour == dn:
				temp_list[dn] = r['time']
				break
	info_to_return = {'campaign': url, 'data': temp_list, 'year': year, 'month': get_month_name(m), 'hours': ['hours'] + get_hours(), 'day': d}
	return render(request, 'report/campaign_hour.html', locals())




##### Dashboard ##########
@login_required
def dashboard_user(request):
	import operator
	dominios = URLAccount.objects.filter(owner=request.user)
	domains = dominios.values_list('domain', flat=True)
	qs = reduce(operator.or_, (VisitorTrack.objects.filter(url_visited__contains=item) for item in domains))
	total = qs.count()
	by_domains = []
	for dom in domains:
		l = qs.filter(url_visited__contains=dom)
		by_domains.append([str(dom), calculate_percentage(total, l.count())])
	by_campaign = []
	new_qs = qs.filter(campaign_key__isnull=False).order_by('campaign_key')
	total_campaign = new_qs.count()
	for m,g in itertools.groupby(new_qs, lambda x: x.campaign_key):
		by_campaign.append([str(m), calculate_percentage(total_campaign, len(list(g)))])
	names_campaign = {}
	values_campaigns =  new_qs.values('campaign', 'campaign_key')
	for i,v in enumerate(values_campaigns):
		names_campaign[str(values_campaigns[i]['campaign_key'])] = str(values_campaigns[i]['campaign'])
	return render(request, 'report/dashboard.html', locals())

###By campaign #######3

@login_required
def report_campaign_view(request):
	
	c = request.GET.get('c')
	if not c:
		raise Http404

	truncate_date = connection.ops.date_trunc_sql('year', 'datetime')
	qs = VisitorTrack.objects.filter(campaign_key=c).extra({'year':truncate_date})
	report = qs.values('year').annotate(time=Sum('time_remained_seconds')).order_by('year')
	print report
	temp_list = ['Tiempo visitado en segundos']
	years_list = ['years']

	for data in report:
		temp_list.append(data['time'])
		years_list.append(data['year'].year)
	info_to_return = {'c': c, 'data': temp_list, 'years': years_list}
	
	return render(request, 'report/campaign.html', locals())


@login_required
def report_campaign_year_view(request):
	campaign = request.GET.get('c')
	year = request.GET.get('y')
	if not campaign or not year:
		raise Http404
	truncate_date = connection.ops.date_trunc_sql('month', 'datetime')
	qs = VisitorTrack.objects.filter(campaign_key=campaign, datetime__year=year).extra({'month':truncate_date})
	report = qs.values('month').annotate(time=Sum('time_remained_seconds')).order_by('month')

	months = get_months()
	num_months = len(months)
	temp_list = ['Tiempo visitado en segundos',0,0,0,0,0,0,0,0,0,0,0,0]
	for mn in range(1, num_months):
		for r in report:
			if r['month'].month == mn:
				temp_list[mn] = r['time']
				break
	info_to_return = {'campaign': campaign, 'data': temp_list, 'months': ['meses'] + get_months(), 'year': year}
	return render(request, 'report/campaign_year.html', locals())

@login_required
def report_campaign_month_view(request):
	campaign = request.GET.get('c')
	year = request.GET.get('y')
	m = request.GET.get('m')
	if not campaign or not year or not m:
		raise Http404
	truncate_date = connection.ops.date_trunc_sql('day', 'datetime')
	qs = VisitorTrack.objects.filter(campaign_key=campaign, datetime__year=year, datetime__month=m).extra({'day':truncate_date})
	report = qs.values('day').order_by('datetime__day').annotate(time=Sum('time_remained_seconds')).order_by('day')
	number_days = get_number_days_month(int(year), int(m))
	temp_list = ['Tiempo visitado en segundos'] + ([0] * number_days[1])
	print report
	for dn in range(1, number_days[1]):
		for r in report:
			if r['day'].day == dn:
				temp_list[dn] = r['time']
				break
	info_to_return = {'campaign': campaign, 'data': temp_list, 'year': year, 'month': get_month_name(m), 'days': ['dias'] + range(1, number_days[1]+1)}
	return render(request, 'report/campaign_daily.html', locals())


@login_required
def report_campaign_day_view(request):
	campaign = request.GET.get('c')
	year = request.GET.get('y')
	m = request.GET.get('m')
	d = request.GET.get('d')
	if not campaign or not year or not m or not d:
		raise Http404
	truncate_date = connection.ops.date_trunc_sql('hour', 'datetime')
	qs = VisitorTrack.objects.filter(campaign_key=campaign, datetime__year=year, datetime__month=m, datetime__day=d).extra({'hour':truncate_date})
	report = qs.values('hour').order_by('datetime__hour').annotate(time=Sum('time_remained_seconds')).order_by('hour')
	
	hours = get_hours()
	temp_list = ['Tiempo visitado en segundos'] + ([0] * 24)
	for dn in hours:
		for r in report:
			hour = r['hour'].hour
			if r['hour'].hour == 0:
				hour = 24
			if hour == dn:
				temp_list[dn] = r['time']
				break
	info_to_return = {'campaign': campaign, 'data': temp_list, 'year': year, 'month': get_month_name(m), 'hours': ['hours'] + get_hours(), 'day': d}
	return render(request, 'report/campaign_hour.html', locals())