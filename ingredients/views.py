from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from ingredients.models import Ingredient
from .forms import IngredientForm

# Create your views here.
class IngredientListView(ListView):
    model = Ingredient
    context_object_name = 'ingredients'
    template_name = 'ingredients/ingredient_list.html'

    def get_queryset(self):
        # Sort the ingredients alphabetically by name
        return Ingredient.objects.all().order_by("name")
    
class IngredientDetailView(DetailView):
    model = Ingredient
    context_object_name = 'ingredient'
    template_name = 'ingredients/ingredient_detail.html'
    
class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients/ingredient_create.html'
    success_url = reverse_lazy('ingredient-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'"{self.object.name}" successfully added.')
        return response
    
class IngredientEditView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients/ingredient_create.html'
    success_url = reverse_lazy('ingredient-list')
    