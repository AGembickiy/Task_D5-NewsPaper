from django.urls import path
from .views import PostList, PostDetail, Posts, PostSearch, PostAdd, UpdatePost, PostDelete

app_name = 'news'

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('<int:pk>/', PostDetail.as_view(), name='news_id'),
    path('search/', PostSearch.as_view(), name='search'),
    path('add/', PostAdd.as_view(), name='add'),
    path('<int:pk>/edit/', UpdatePost.as_view(), name='edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
]

