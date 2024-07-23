from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('category-list/', views.CategoryListView.as_view(), name='category_list'),
    path('', views.GoodsListView.as_view(), name='goods_list'),
    path('category/<str:category>/', views.GoodsListView.as_view(), name='goods_category_list'),
    path('<int:pk>', views.GoodsDetailView.as_view(), name='goods_detail'),
    path('<int:pk>/comment-create/', views.CommentCreateView.as_view(),
         name='comment_create'),
    path('comment/<int:pk>/', views.CommentUpdateDeleteView.as_view(),
         name='comment_edit')
]
