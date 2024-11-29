from django.urls import path
from .views import IngredientListView, IngredientDetailView, IngredientCreateView, IngredientEditView, ConfirmIngredientDeleteView, IngredientDeleteView

urlpatterns = [
    path('',IngredientListView.as_view(),name='ingredient-list'),
    path('details/<int:pk>/',IngredientDetailView.as_view(),name='ingredient-detail'),
    path('edit/<int:pk>/',IngredientEditView.as_view(),name='ingredient-edit'),
    path('delete/<int:pk>/',IngredientEditView.as_view(),name='ingredient-delete'),
    path('create/',IngredientCreateView.as_view(),name='ingredient-create'),
    path('delete_ingredient/<int:pk>/',IngredientDeleteView.as_view(),name='delete-ingredient'),
    path('confirm-ingredient-delete/<int:pk>/',ConfirmIngredientDeleteView.as_view(),name='confirm-ingredient-delete'),
]
