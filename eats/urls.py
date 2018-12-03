from django.urls import path
from .models import Eat, Hour
from . import views

app_name = 'eats'

urlpatterns = [
    path('', views.EatList.as_view(), name='index'),
    path('<int:pk>/', views.EatDetail.as_view(), name='detail'),
    # path('map/', views.map, name = 'map'),
    path('maplist/', views.MapList.as_view(), name='maplist'),
]