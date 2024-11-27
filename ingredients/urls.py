from django.urls import path
from .views import IngredientListView, IngredientDetailView, IngredientCreateView, IngredientEditView

urlpatterns = [
    path('',IngredientListView.as_view(),name='ingredient-list'),
    path('details/<int:pk>/',IngredientDetailView.as_view(),name='ingredient-detail'),
    path('edit/<int:pk>/',IngredientEditView.as_view(),name='ingredient-edit'),
    path('delete/<int:pk>/',IngredientEditView.as_view(),name='ingredient-delete'),
    path('create/',IngredientCreateView.as_view(),name='ingredient-create'),
]
