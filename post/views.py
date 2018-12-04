from django.shortcuts import render,get_object_or_404, resolve_url, redirect
from django.views.generic import ListView, CreateView,DetailView,DeleteView,UpdateView
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.urls import reverse_lazy

# Create your views here.

class PostList(ListView):
    model = Post
    context_object_name = 'post'
    template_name = 'post/post_list.html'
    ordering=['-id']
    # def get_context_data(self, **kwargs):
    #     q = self.request.GET.get('q', '') 
    #     context = super().get_context_data(**kwargs)
    #     post_list = Post.objects.filter(title__icontains=q) 
    #     context['post'] = post_list
    #     return context
        
    def get_queryset(self):
        
        q = self.request.GET.get('q', False) 
        anon = self.request.GET.get('anon', 'false')
        print(anon)
        if anon == 'true':
            category = '1'
        else:
            category = '2'
                
        if q:
            paginator = Paginator(Post.objects.filter(category=category, title__contains=q), 5) # Show 25 contacts per page
        else:
            paginator = Paginator(Post.objects.filter(category=category), 5) # Show 25 contacts per page
        page = self.request.GET.get('page')
        return paginator.get_page(page)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # post_list = Post.objects.filter(category="1")
        context['anon'] = self.request.GET.get('anon', 'false')
        return context

        
    
class UnNamedPostList(ListView):
    model = Post
    context_object_name = 'post'
    template_name = 'post/post_list.html'
    
    def get_queryset(self):
        # q = self.request.GET.get('q', '') 
        # if q:
        paginator = Paginator(Post.objects.filter(category="1"), 5) # Show 25 contacts per page
        # else:
        #     paginator = Paginator(Post.objects.all(), 5) # Show 25 contacts per page
        page = self.request.GET.get('page')
        return paginator.get_page(page)
        # paginator = Paginator(Post.objects.filter(category="1"), 5) # Show 25 contacts per page
        # page = self.request.GET.get('page')
        # return paginator.get_page(page)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # post_list = Post.objects.filter(category="1")
        context['category'] = "1"
        return context
        
    # def search(request):
    #     qs = Post.objects.all()
    
    #     q = request.GET.get('q', '') 
    #     if q:
    #         qs = qs.filter(Post.title=q) 
    
    #     return render(request, 'post/post_list.html', {
    #         'post_list' : qs,
    #         'q' : q,
    #     })        
    
class NamedPostList(ListView):
    model = Post    
    template_name = 'post/post_list.html'
    context_object_name = 'post'
    def get_queryset(self):
        q = self.request.GET.get('q', '') 
        if q:
            paginator = Paginator(Post.objects.filter(category="2"), 5) # Show 25 contacts per page
        else:
            paginator = Paginator(Post.objects.all(), 5) # Show 25 contacts per page
        page = self.request.GET.get('page')
        return paginator.get_page(page)


        # paginator = Paginator(Post.objects.filter(category="2"), 5) # Show 25 contacts per page
        # page = self.request.GET.get('page')
        # return paginator.get_page(page)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # post_list = Post.objects.filter(category="1")
        context['category'] = "2"
        return context

    # def search(request):
    #     qs = Post.objects.all()
    
    #     q = request.GET.get('q', '') # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    #     if q: # q가 있으면
    #         qs = qs.filter(Post.title=q) # 제목에 q가 포함되어 있는 레코드만 필터링
    
    #     return render(request, 'post/post_list.html', {
    #         'post_list' : qs,
    #         'q' : q,
    #     })       

    
class PostCreate(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content',]
    
    def form_valid(self,form):
        category = self.request.GET.get('category')
        self.object = form.save(commit=False)
        self.object.category = category
        self.object.save()
        return super().form_valid(form)
        
    # def search(request):
    #     qs = Post.objects.all()
    #     q = request.GET.get('q', '') # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    #     if q: # q가 있으면
    #         qs = qs.filter(Post.title=q) # 제목에 q가 포함되어 있는 레코드만 필터링
    
    #     return render(request, 'post/post_list.html', {
    #         'post_list' : qs,
    #         'q' : q,
    #     })   

class PostDetail(DetailView):
    model = Post
    
    def get_object(self):
        post = Post.objects.prefetch_related('comment_set__user').select_related('user')
        return get_object_or_404(post, pk=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
        
class PostDelete(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post:list')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)
        
   
class PostUpdate(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ('content',)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)        
        
class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content',]
    
    def form_valid(self,form):
        post = Post.objects.get(id = self.kwargs.get('pk'))
        self.object = form.save(commit=False)
        self.object.post = post
        self.object.user = self.request.user
        self.object.save()
        
        return super().form_valid(form)

# 로그인했니??
@login_required
def like(request,pk):
    if request.is_ajax():
        user = request.user
        post = Post.objects.get(pk=pk)
        
        # 사용자가 like를 눌렀으면 취소
        if post.like.filter(id=user.id).exists():
            post.like.remove(user)
        # 안눌렀으면 좋아요
        else:
            post.like.add(user)
        data = {'likes_count' : post.like.count()}
        return HttpResponse(json.dumps(data), content_type="application/json")
        
    else:
        return redirect( resolve_url('post:detail',pk) )
        
# 로그인했니??
@login_required
def comment_like(request,pk):
    if request.is_ajax():
        user = request.user
        comment = Comment.objects.get(pk=pk)
        
        # 사용자가 like를 눌렀으면 취소
        if comment.like.filter(id=user.id).exists():
            comment.like.remove(user)
        # 안눌렀으면 좋아요
        else:
            comment.like.add(user)
        data = {'likes_count' : comment.like.count()}
        return HttpResponse(json.dumps(data), content_type="application/json")
        
    else:
        return redirect( resolve_url('post:detail',pk) )        
