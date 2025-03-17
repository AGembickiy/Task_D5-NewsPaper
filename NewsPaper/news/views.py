from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    ordering = ['-date_time_creation']
    paginate_by = 1


class PostDetail(DetailView):
    model = Post
    template_name = 'news/newid.html'
    context_object_name = 'newid'


class Posts(View):

    def get(self, request):
        posts = Post.objects.order_by('-date_time_creation')
        p = Paginator(posts, 1)
        posts = p.get_page(request.GET.get('page', 1))
        data = {'posts': posts, }

        return render(request, 'news/paginator.html', data)


class PostSearch(ListView):
    model = Post
    template_name = 'news/search.html'
    form_class = PostFilter
    context_object_name = 'search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostFilter()
        return context
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class PostAdd(CreateView):
    template_name = 'news/add.html'
    form_class = PostForm



class UpdatePost(UpdateView):
    template_name = 'news/add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
       id = self.kwargs.get('pk')
       return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/delete.html'
    context_object_name = 'newid'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news:home')


