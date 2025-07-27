from django.urls import path
from .views import BlogListView, BlogDetailView, PostByCategoryView, PostByTagView


app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='post_list'), 
    path('<slug:slug>/', BlogDetailView.as_view(), name='post_detail'),
    path('category/<str:category_name>/', PostByCategoryView.as_view(), name='post_by_category'),
    path('tag/<str:tag_name>/', PostByTagView.as_view(), name='post_by_tag'),
]