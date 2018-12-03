from django.db import models
from django.db.models import Q
from datetime import timezone, timedelta, datetime


# Create your models here.
class Hour(models.Model):
    is_hol = models.BooleanField()
    day = models.CharField(max_length=10)
    open = models.TimeField(blank=True, null=True)
    close = models.TimeField(blank=True, null=True)
    last = models.TimeField(blank=True, null=True)
    day_note = models.CharField(max_length=50)
    etc = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return str(self.day) + ' : ' + str(self.open) +' ~ '+str(self.close)
        
class Eat(models.Model):
    name = models.CharField(max_length=30)
    addr = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    time = models.ManyToManyField(Hour,related_name='time',blank=True)
    x = models.FloatField()
    y = models.FloatField()
    imgSrc = models.URLField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
        
    def is_open(self):
        now = datetime.now()
        time = {'day': now.weekday(), 'time': now.time()}
        day_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        
        # 현재시간이 24:00 이전이면서 close가 24:00 이전일때
        res = self.time.filter(Q(day = day_list[time['day']]) & Q(open__lte = time['time']) & Q(close__gte = time['time']))

        try:
            res[0]
        except IndexError:
            return False
        else:
            return True
            
            
    