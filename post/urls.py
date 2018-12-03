from django.urls import path
from . import views

app_name='post'
urlpatterns = [
    path('',views.PostList.as_view(),name='list'),
    path('unnamed/',views.UnNamedPostList.as_view(),name='unnamed'),
    path('named/',views.NamedPostList.as_view(),name='named'),
    path('create/',views.PostCreate.as_view(),name='create'),
    path('<pk>/',views.PostDetail.as_view(),name='detail'),
    path('<int:pk>/comments',views.CommentCreate.as_view(),name="comment_create"),
    path('<int:pk>/like/', views.like ,name='like'),
    path('<int:pk>/comment_like/', views.comment_like, name='comment_like'),
    path('delete/<pk>/',views.PostDelete.as_view(),name='delete'),
    path('update/<pk>/',views.PostUpdate.as_view(),name='update'),
    # path('search/', views.PostSearch.as_view(),name='search'),
]

