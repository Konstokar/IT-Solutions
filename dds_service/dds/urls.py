from django.urls import path
from .views import (
    MoneyMovementListView,
    MoneyMovementCreateView,
    MoneyMovementUpdateView,
    MoneyMovementDeleteView,
    load_categories,
    load_subcategories
)

urlpatterns = [
    path('', MoneyMovementListView.as_view(), name='money_movement_list'),
    path('new/', MoneyMovementCreateView.as_view(), name='money_movement_create'),
    path('<int:pk>/edit/', MoneyMovementUpdateView.as_view(), name='money_movement_update'),
    path('<int:pk>/delete/', MoneyMovementDeleteView.as_view(), name='money_movement_delete'),
    path('load-categories/', load_categories, name='load_categories'),
    path('load-subcategories/', load_subcategories, name='load_subcategories'),
]