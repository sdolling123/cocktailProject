from django.shortcuts import render, redirect, get_object_or_404
from formtools.wizard.views import SessionWizardView
from .models import Cocktail, CocktailIngredient
from .forms import CocktailBasicDetailsForm, CocktailIngredientsForm, CocktailInstructionsForm, PlaceholderForm, SelectIngredientsForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView
from ingredients.models import Ingredient

# Create your views here.
class CocktailListView(ListView):
    model = Cocktail
    context_object_name = 'cocktails'
    template_name = 'cocktails/cocktail_list.html'

    def get_queryset(self):
        # Sort the ingredients alphabetically by name
        return Cocktail.objects.all().order_by("name")

FORMS = [
    ('cocktail-overview',CocktailBasicDetailsForm),
    ('add-ingredient',PlaceholderForm),
    ('cocktail-instructions',CocktailInstructionsForm),
]

class CocktailCreationWizard(SessionWizardView):
    form_list = FORMS
    template_name = 'cocktails/cocktail_create.html'

    def done(self, form_list, **kwargs):
        """
        This is called when the wizard is completed.
        form_list contains all the validated form data.
        """
        # Save basic details form
        basic_details_form = form_list[0]
        cocktail = basic_details_form.save()

        # Save ingredients form
        ingredients_form = form_list[1]
        for ingredient in ingredients_form.cleaned_data['ingredients']:
            CocktailIngredient.objects.create(
                cocktail=cocktail,
                ingredient=ingredient,
                quantity=ingredients_form.cleaned_data['quantity'],
                unit=ingredients_form.cleaned_data['unit']
            )

        # Save instructions form
        instructions_form = form_list[2]
        cocktail.instructions = instructions_form.cleaned_data['instructions']
        cocktail.save()

        # Add a success message
        messages.success(self.request, f"The cocktail '{cocktail.name}' was successfully added!")

        # Redirect to the cocktail list page
        return redirect('cocktail-list')

class SelectIngredientsView(FormView):
    template_name = "cocktails/select_ingredients.html"
    form_class = SelectIngredientsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cocktail"] = get_object_or_404(Cocktail, pk=self.kwargs["pk"])
        return context

    def get_form(self):
        """Override to pre-select ingredients already associated with the cocktail."""
        form = super().get_form()
        cocktail = get_object_or_404(Cocktail, pk=self.kwargs["pk"])
        # Get the ingredients already linked to this cocktail
        selected_ingredients = Ingredient.objects.filter(
            id__in=cocktail.ingredients.values_list("ingredient_id", flat=True)
        )
        # Pre-select these ingredients in the form
        form.fields["ingredients"].initial = selected_ingredients
        return form

    def form_valid(self, form):
        cocktail = get_object_or_404(Cocktail, pk=self.kwargs["pk"])
        selected_ingredients = form.cleaned_data["ingredients"]

        # Update the cocktail's ingredients
        # Remove ingredients no longer selected
        CocktailIngredient.objects.filter(cocktail=cocktail).exclude(
            ingredient__in=selected_ingredients
        ).delete()

        # Add new ingredients
        for ingredient in selected_ingredients:
            CocktailIngredient.objects.get_or_create(
                cocktail=cocktail,
                ingredient=ingredient,
                defaults={"quantity": 0, "unit": ""},
            )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cocktail-list")