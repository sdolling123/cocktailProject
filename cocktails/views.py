from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from .models import Cocktail, CocktailIngredient
from .forms import CocktailBasicDetailsForm, CocktailIngredientsForm, CocktailInstructionsForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView

# Create your views here.
class CocktailListView(ListView):
    model = Cocktail
    context_object_name = 'cocktails'
    template_name = 'cocktails/cocktail_list.html'

    def get_queryset(self):
        # Sort the ingredients alphabetically by name
        return Cocktail.objects.all().order_by("name")
    
class CocktailCreationWizard(SessionWizardView):
    form_list = [CocktailBasicDetailsForm, CocktailIngredientsForm, CocktailInstructionsForm]
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
