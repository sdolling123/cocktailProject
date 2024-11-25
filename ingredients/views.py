from django.shortcuts import render
from django.views.generic import ListView
from ingredients.models import Ingredient

# Create your views here.
class IngredientListView(ListView):
    model = Ingredient
    context_object_name = 'ingredients'
    template_name = 'ingredients/ingredient_list.html'

    def get_queryset(self):
        # Sort the ingredients alphabetically by name
        return Ingredient.objects.all().order_by("name")