from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import status
from rest_framework import mixins
from django.db.models import Case, When
from django.contrib.auth import get_user_model
from .models import Category, Goods, Comment
from .permissions import IsAuthor # IsGoodsBoughtByUser
from .generics_views import UpdateDestroyAPIView
from . import serializers


class CategoryListView(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all


class GoodsListView(generics.ListAPIView):
    serializer_class = serializers.GoodsListSerializer

    def get_queryset(self):
        category = self.kwargs.get('category')
        queryset = Goods.objects.all().select_related ('category').only(
            'image', 'title', 'price', 'rating', 'category__title'
        )
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if title or category:
            '''
            если пользователь фильтрует товары по категории или по названию --> он не просто
            просматривает список всех товаров, а пришёл с какой-то конкретной целью и просматривает
            определённый диапазон товаров --> предлагаем ему отфильтровать по цене
            '''
            allowable_price = self.request.query_params.get('price', None)
            if allowable_price:
                min_val, max_val = map(float, allowable_price.split(';'))
                queryset = queryset.filter(price__gte=min_val, price__lte=max_val)
        if not category:
            '''
            если не фильтрует по категориям --> сортируем результат по товарам с теми категориями,
            с которыми пользователь уже покупал какие-то товары
            '''
            if self.request.user.is_authenticated:
                user = get_user_model().objects.get(id=self.request.user.id)
                categories_bought = user.categories_bought
                if categories_bought:
                    sorted_categories_bought = sorted(
                        categories_bought.items(),
                        key=lambda category: category[1],
                        reverse=True
                    )
                    sorted_categories_bought = [
                        category for category, count in sorted_categories_bought
                    ]
                    '''
                    case = Case(
                        *[When(category__name=cat, then=ord) for ord, cat
                          in enumerate(sorted_categories_bought)]
                    )
                    '''
                    recommended_goods_list = []
                    for category in sorted_categories_bought:
                        '''
                        Предлагаем пользователю сначала персональные предложения для его, ограниченный
                        суммарным количеством до 25, и чтобы обеспечить, что эти товары будут из разных
                        категорий, для 1 категории ограничиваем количество товаров до 2.
                        В результате если мы имеем 9 категорий и 1000 товаров этих категорий,
                        всего в рекомендации попадёт 18 товаров. 
                        '''
                        category_goods = queryset.filter(category__title=category).order_by(
                            '-times_bought'
                        )[:2]
                        recommended_goods_list.extend(category_goods)
                        if len(recommended_goods_list) >= 25:
                            break
        
                    other_goods = queryset.exclude(
                        id__in=[good.id for good in recommended_goods_list]
                    ).order_by('-times_bought')

                    combined_goods_list = recommended_goods_list + list(other_goods)
                    combined_ids = [good.id for good in combined_goods_list]
                    '''
                    формируем итоговый queryset из объединенного списка combined_ids таким образом,
                    чтобы в итоговом queryset объекты шли таким же образом, как и id объектов в combined_ids
                    '''
                    queryset = Goods.objects.filter(id__in=combined_ids).order_by(
                        Case(
                            *[When(pk=pk, then=pos) for pos, pk in enumerate(combined_ids)]
                        )
                    )
                    return queryset
        else:
            # если категория пристутствует в url - отображаем товары с этой категорией
            queryset = Goods.objects.filter(category__title__iexact=category)
        queryset = queryset.order_by('-times_bought')
        return queryset
    

class GoodsDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.GoodsDetailSerializer
    queryset = Goods.objects.all()


class CommentCreateView(generics.CreateAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated] #, IsGoodsBoughtByUser() ]


class CommentUpdateDeleteView(UpdateDestroyAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated()] #, IsGoodsBoughtByUser() ]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAuthor()]
        return []