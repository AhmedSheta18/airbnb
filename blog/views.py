from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category
from taggit.models import Tag
from django.db.models import Count, Q

# Create your views here.




class BlogListView(ListView):
    model = Post
    paginate_by = 6 

    def get_queryset(self):
        search = self.request.GET.get('q', '')
        object_list = Post.objects.filter(
            Q(title__icontains = search) |
            Q(content__icontains = search) 
        )
        return object_list






class BlogDetailView(DetailView):
    model = Post


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().annotate(post_count=Count('post_category'))

        context["tags"] = Tag.objects.all()
        context["recent_posts"] = Post.objects.order_by('-created_at').exclude(id=self.object.id)[:3]
        return context
    

class PostByCategoryView(ListView):
    model = Post
    paginate_by = 6

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        object_list = Post.objects.filter(
            Q(category__name__icontains=category_name)
        )
        return object_list

class PostByTagView(ListView):
    model = Post
    paginate_by = 6

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        object_list = Post.objects.filter(
            Q(tags__name__icontains=tag_name)
        )
        return object_list
