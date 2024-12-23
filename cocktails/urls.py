from django.urls import path
from .views import CocktailListView, CocktailCreationWizard, SelectIngredientsView, CocktailWizardView, CocktailDetailView, CocktailTabbed
from ingredients.views import IngredientComponentListView

urlpatterns = [
    path('',CocktailListView.as_view(),name='cocktail-list'),
    path('create/',CocktailCreationWizard.as_view(),name='cocktail-create'),
    path('cocktail-wizard/',CocktailWizardView.as_view(),name='cocktail-wizard'),
    path('cocktail-tabbed/',CocktailTabbed.as_view(),name='cocktail-tabbed'),
    path('create/ingredient-search/',IngredientComponentListView.as_view(),name='cocktail-ingredient-search'),
    path("cocktail/<int:pk>/select-ingredients/", SelectIngredientsView.as_view(), name="select_ingredients"),
    path("cocktail/<int:pk>/details/", CocktailDetailView.as_view(), name="cocktail-details"),
    # path('details/<int:pk>/',IngredientDetailView.as_view(),name='ingredient-detail'),
    # path('edit/<int:pk>/',IngredientEditView.as_view(),name='ingredient-edit'),
    # path('delete/<int:pk>/',IngredientEditView.as_view(),name='ingredient-delete'),
    # path('delete_ingredient/<int:pk>/',IngredientDeleteView.as_view(),name='delete-ingredient'),
    # path('confirm-ingredient-delete/<int:pk>/',ConfirmIngredientDeleteView.as_view(),name='confirm-ingredient-delete'),
]
