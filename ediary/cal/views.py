import calendar
from pkgutil import get_data
from django.shortcuts import get_object_or_404, redirect, render
from datetime import date, datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator

from .forms import EventForm

from .models import *
from .utils import Calendar
# Create your views here.
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar.html'
    
    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            # print("asdf")
            # print(self.request.user)
            context = super().get_context_data(**kwargs)
            d = get_date(self.request.GET.get('month', None))
            print("====",self.request.user)
            cal = Calendar(d.year, d.month, self.request.user)
            html_cal = cal.formatmonth(withyear=True)
            context['calendar'] = mark_safe(html_cal)
            context['prev_month'] = prev_month(d)
            context['next_month'] = next_month(d)
            # print(context)
            return context
        else:
            return redirect('login')
    
def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    print(month)
    return month

# def event(request, event_id=None):
#     instance = Event()
#     if event_id:
#         instance = get_object_or_404(Event, pk=event_id)
#     else:
#         instance = Event()
    
#     form = EventForm(request.POST or None, instance=instance)
#     if request.POST and form.is_valid():
#         form.save()
#         return HttpResponseRedirect(reverse('calendar'))
#     return render(request, 'event.html', {'form': form}) 



@login_required
def event(request, event_id=None):
    if request.method == 'POST':
        user=request.user
        title = request.POST['eventName']
        description = request.POST['eventDescription']
        start_time = request.POST['startDate']
        end_time = request.POST['endDate']
        event=Event.objects.create(user=user,title=title,description=description,start_time=start_time,end_time=end_time)
        event.save
        return redirect('calendar')
    
    else:
        return render(request, 'eventss.html')
@login_required  
def editevent(request, event_id):
    instance = Event.objects.get(id=event_id)
    if request.method == 'POST':
        instance.title = request.POST.get('eventName')
        instance.description = request.POST.get('eventDescription')
        instance.start_time = request.POST.get('startDate')
        instance.end_time = request.POST.get('endDate')
        instance.save()
        return redirect('calendar')
        # user=request.user
        # title = request.POST['eventName']
        # description = request.POST['eventDescription']
        # start_time = request.POST['startDate']
        # end_time = request.POST['endDate']
        # event=Event.objects.get(id=event_id)

    else:
        #event=Event.objects.get(id=event_id)
        return render(request, 'editevent.html', {"instance":instance})
@login_required  
def adddiary(request):
    print(request.method)
    if request.method == 'POST':
        user=request.user
        title = request.POST['title']
        text = request.POST['entry']
        entry = Entry.objects.create(user=user,title = title, text=text)
        print(text)
        entry.save()
        return redirect('diaryview')
    else:    
        return render(request, 'diary.html')




@login_required(login_url="login")
def diaryview(request):
    entries = Entry.objects.filter(user=request.user).order_by('-date_posted')
    context = {'entries' : entries}
    return render(request, 'viewdiary.html' , context)
    
@login_required
def view(request,id):
    print(id)
    entry = Entry.objects.get(id=id) 
    print(entry)
    context = {'entry':entry}
    return render(request, 'view.html' , context)
@login_required
def editdiary(request,id): 
    instance = Entry.objects.get(id=id)
    if request.method == 'POST':
        instance.title = request.POST.get('title')
        instance.text = request.POST.get('entry')
        instance.save()
        return redirect(diaryview)
        
    return render(request, 'editdiary.html',{'instance':instance})
     
 
