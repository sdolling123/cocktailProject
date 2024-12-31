from django.urls import path
from .views import CocktailListView, CocktailDetailView, CocktailTabbed, CocktailIngredientOptions, EditCocktailView,DeleteCocktailView,ConfirmCocktailDeleteView
from ingredients.views import IngredientComponentListView

urlpatterns = [
    path('',CocktailListView.as_view(),name='cocktail-list'),
    path('ingredient-options/',CocktailIngredientOptions.as_view(),name='ingredient-options'),
    path('cocktail-tabbed/',CocktailTabbed.as_view(),name='cocktail-tabbed'),
    path('create/ingredient-search/',IngredientComponentListView.as_view(),name='cocktail-ingredient-search'),
    path("cocktail/<int:pk>/details/", CocktailDetailView.as_view(), name="cocktail-details"),
    path("cocktail/<int:pk>/edit/", EditCocktailView.as_view(), name="cocktail-edit"),
    path("confirm-cocktail-delete/<int:pk>/delete/", DeleteCocktailView.as_view(), name="cocktail-delete"),
    path("cocktail/<int:pk>/delete/", ConfirmCocktailDeleteView.as_view(), name="cocktail-confirm-delete"),
]
