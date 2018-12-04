from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .models import Eat, Hour
from datetime import timezone, timedelta, datetime
import math


# Create your views here.
class EatList(ListView):
    model = Eat
    template_name = 'eats/index.html'
    context_object_name = 'eats'
    
    def get_queryset(self):
        queryset = Eat.objects.all()
        paginator = Paginator(queryset, 15)
        page = self.request.GET.get('page')
        return paginator.get_page(page)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.GET.get('search', False):
            output = Eat.objects.filter(Q(name__contains=self.request.GET['search']) |
                                        Q(addr__contains=self.request.GET['search']))
        else:
            output = Eat.objects.all()
        
        if self.request.GET.get('status') == 'open':
            tz = timezone(timedelta(hours=9))
            now = datetime.now()
            time = {'day': now.weekday(), 'time': now.time()}
            day_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
            output = output.filter(Q(time__day = day_list[time['day']]) &
                                      Q(time__open__lte = time['time']) &
                                      Q(time__close__gte = time['time']))
        
        paginator = Paginator(output, 15)
        page = self.request.GET.get('page')
        
        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
        
        context['results'] = file_exams
        
        return context
    
    
class EatDetail(DetailView):
    model = Eat
    template_name = 'eats/detail.html'
    context_object_name = 'eat'
    
    
    
class MapList(ListView):
    model = Eat
    template_name = 'eats/maplist.html'
    
    def get_queryset(self):
        queryset = Eat.objects.all()
        paginator = Paginator(queryset, 15)
        page = self.request.GET.get('page')
        return paginator.get_page(page)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.GET.get('search', False):
            output = Eat.objects.filter(Q(name__contains=self.request.GET['search']) |
                                        Q(addr__contains=self.request.GET['search']))
        else:
            output = Eat.objects.all()
        
        if self.request.GET.get('status') == 'open':
            tz = timezone(timedelta(hours=9))
            now = datetime.now()
            time = {'day': now.weekday(), 'time': now.time()}
            day_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
            output = output.filter(Q(time__day = day_list[time['day']]) &
                                      Q(time__open__lte = time['time']) &
                                      Q(time__close__gte = time['time']))
        
        paginator = Paginator(output, 15)
        page = self.request.GET.get('page')
        
        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
        
        context['results'] = file_exams
        
        
        return context
        
def map(request):
    location = [[37.5018216, 127.0355291],[37.50329,127.0414513],[37.5018498,127.0366247],[37.5089909,127.0381735],[37.5019224,127.0372503]]
    return render(request,'eats/map.html', {'location':location})
    

def getposition(request):
    # user = request.user
    ajaxPosition = request.POST.get('ajaxPosition', None)
    position = ajaxPosition.split('&')
    # 필터수정
    # positions = Eat.objects.all().filter(math.sqrt((self.x-float(position[0]))**2+(self.y-float(position[1]))**2)<int(position[2]))

    data = {'positions' : positions}
    return HttpResponse(json.dumps(data), content_type="application/json")