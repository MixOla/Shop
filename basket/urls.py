from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('add/', views.BasketAddGoodsView.as_view(), name='basket_add_goods'),
    path('remove/', views.BasketRemoveGoodsView.as_view(), name='basket_remove_goods'),
    path('detail/', views.BasketDetailView.as_view(), name='basket_detail'),
]
