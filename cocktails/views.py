from django.shortcuts import render, redirect, get_object_or_404
from formtools.wizard.views import SessionWizardView
from .models import Cocktail, CocktailIngredient
from .forms import CocktailBasicDetailsForm, CocktailIngredientsForm, CocktailInstructionsForm, PlaceholderForm, SelectIngredientsForm, AddIngredientDetailsForm, CocktailForm, CocktailIngredientForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from ingredients.models import Ingredient
from django.forms import formset_factory

# Create your views here.

class CocktailTabbed(TemplateView):
    def get(self, request):
        cocktail_form = CocktailForm()
        ingredient_form = CocktailIngredientForm()
        return render(request, 'cocktails/cocktail_tabbed_exp.html', {
            'cocktail_form': cocktail_form,
            'ingredient_form': ingredient_form
        })

    def post(self, request):
        cocktail_form = CocktailForm(request.POST)
        print("cocktail form", cocktail_form)
        # Extract ingredient data grouped by UUID
        print("ingredient form", request.POST.items())
        ingredient_data = {}
        for key, value in request.POST.items():
            print("key: ",key)
            print("value: ", value)
            if key.startswith("ingredient_id_"):
                uuid = key.split("_")[-1]
                ingredient_data.setdefault(uuid, {})['ingredient'] = value
            elif key.startswith("ingredient_quantity_"):
                uuid = key.split("_")[-1]
                ingredient_data.setdefault(uuid, {})['quantity'] = value
            elif key.startswith("ingredient_unit_"):
                uuid = key.split("_")[-1]
                ingredient_data.setdefault(uuid, {})['unit'] = value

        print("Ingredient Data:", ingredient_data)  # Debugging

        if cocktail_form.is_valid():
            # Save the cocktail
            cocktail = cocktail_form.save()

            # Process each set of ingredient data
            ingredient_forms = []
            for uuid, data in ingredient_data.items():
                ingredient_form = CocktailIngredientForm(data)
                ingredient_forms.append(ingredient_form)

                if ingredient_form.is_valid():
                    ingredient = ingredient_form.save(commit=False)
                    ingredient.cocktail = cocktail
                    ingredient.save()
                else:
                    print("Ingredient Form Errors:", ingredient_form.errors)  # Debugging
                    # If any ingredient form is invalid, return the form with errors
                    return render(request, 'cocktails/cocktail_tabbed_exp.html', {
                        'cocktail_form': cocktail_form,
                        'ingredient_form': CocktailIngredientForm(),
                        'ingredient_forms': ingredient_forms,  # Include all forms for error display
                    })
             # Add a success message
            messages.success(self.request, f"The cocktail '{cocktail.name}' was successfully added!")
            return redirect('cocktail-list')  # Redirect to the cocktail list view

        return render(request, 'cocktails/cocktail_tabbed_exp.html', {
            'cocktail_form': cocktail_form,
            'ingredient_form': CocktailIngredientForm(),
        })

class EditCocktailView(TemplateView):
    def get(self, request, pk):
        cocktail = get_object_or_404(Cocktail, pk=pk)
        cocktail_form = CocktailForm(instance=cocktail)
        ingredient_forms = [
            CocktailIngredientForm(instance=ingredient, prefix=f"ingredient_{ingredient.pk}")
            for ingredient in cocktail.ingredients.all()
        ]

        return render(request, 'cocktails/cocktail_edit.html', {
            'cocktail_form': cocktail_form,
            'ingredient_forms': ingredient_forms,
        })
    def post(self, request, pk):
        cocktail = get_object_or_404(Cocktail, pk=pk)
        cocktail_form = CocktailForm(request.POST, instance=cocktail)
        
        existing_ingredient_ids = set(
            cocktail.ingredients.values_list('id', flat=True)
        )
        
        ingredient_forms = []
        processed_ingredient_ids = set()
        valid = cocktail_form.is_valid()

        # Group form fields by their identifier
        form_groups = {}
        
        for key in request.POST:
            if not key.startswith("ingredient_"):
                continue
                
            print(f"Processing key: {key}")
            
            # Handle existing ingredients (format: ingredient_131-ingredient)
            if '-' in key:
                identifier = key.split('-')[0].split('_')[1]
                if identifier not in form_groups:
                    form_groups[identifier] = 'existing'
                    
            # Handle new ingredients (format: ingredient_id_UUID)
            elif '_id_' in key or '_quantity_' in key or '_unit_' in key:
                identifier = key.split('_')[-1]
                if identifier not in form_groups:
                    form_groups[identifier] = 'new'

        print(f"Form groups: {form_groups}")

        # Process each group of ingredient fields
        for identifier, form_type in form_groups.items():
            print(f"Processing identifier: {identifier}, type: {form_type}")
            
            if form_type == 'existing':
                try:
                    ingredient = CocktailIngredient.objects.get(
                        pk=identifier, 
                        cocktail=cocktail
                    )
                    processed_ingredient_ids.add(int(identifier))
                    prefix = f"ingredient_{identifier}"
                except CocktailIngredient.DoesNotExist:
                    continue
            else:  # new
                ingredient = CocktailIngredient(cocktail=cocktail)
                # Don't use a prefix for new ingredients as the fields already include the UUID
                prefix = "ingredient"
            
            # For debugging, print the POST data for this form
            print(f"POST data for {identifier}:")
            for key, value in request.POST.items():
                if (form_type == 'existing' and f"ingredient_{identifier}-" in key) or \
                (form_type == 'new' and identifier in key):
                    print(f"{key}: {value}")

            ingredient_form = CocktailIngredientForm(
                request.POST,
                instance=ingredient,
                prefix=prefix
            )
            ingredient_forms.append(ingredient_form)
            if not ingredient_form.is_valid():
                valid = False
                print(f"Form errors for {identifier}: {ingredient_form.errors}")

        if valid:
            cocktail = cocktail_form.save()
            
            # Delete ingredients that were removed
            ingredients_to_delete = existing_ingredient_ids - processed_ingredient_ids
            CocktailIngredient.objects.filter(
                id__in=ingredients_to_delete, 
                cocktail=cocktail
            ).delete()
            
            # Save all ingredient forms
            for ingredient_form in ingredient_forms:
                ingredient = ingredient_form.save(commit=False)
                ingredient.cocktail = cocktail
                ingredient.save()

            messages.success(request, f"The cocktail '{cocktail.name}' was successfully updated!")
            return redirect('cocktail-list')

        # If we get here, there were validation errors
        print("Form validation failed")
        for form in ingredient_forms:
            print(f"Form errors: {form.errors}")

        return render(request, 'cocktails/cocktail_edit.html', {
            'cocktail_form': cocktail_form,
            'ingredient_forms': ingredient_forms,
        })

    # def post(self, request, pk):
    #     cocktail = get_object_or_404(Cocktail, pk=pk)
    #     cocktail_form = CocktailForm(request.POST, instance=cocktail)
        
    #     existing_ingredient_ids = set(
    #         cocktail.ingredients.values_list('id', flat=True)
    #     )
        
    #     ingredient_forms = []
    #     processed_ingredient_ids = set()
    #     valid = cocktail_form.is_valid()

    #     # Group form fields by their identifier
    #     form_groups = {}
        
    #     for key in request.POST:
    #         if not key.startswith("ingredient_"):
    #             continue
                
    #         print(f"Processing key: {key}")  # Debug print
            
    #         # Handle existing ingredients (format: ingredient_131-ingredient)
    #         if '-' in key:
    #             identifier = key.split('-')[0].split('_')[1]
    #             if identifier not in form_groups:
    #                 form_groups[identifier] = 'existing'
                    
    #         # Handle new ingredients (format: ingredient_id_UUID)
    #         elif '_id_' in key or '_quantity_' in key or '_unit_' in key:
    #             identifier = key.split('_')[-1]
    #             if identifier not in form_groups:
    #                 form_groups[identifier] = 'new'

    #     print(f"Form groups: {form_groups}")  # Debug print

    #     # Process each group of ingredient fields
    #     for identifier, form_type in form_groups.items():
    #         print(f"Processing identifier: {identifier}, type: {form_type}")  # Debug print
            
    #         if form_type == 'existing':
    #             try:
    #                 ingredient = CocktailIngredient.objects.get(
    #                     pk=identifier, 
    #                     cocktail=cocktail
    #                 )
    #                 processed_ingredient_ids.add(int(identifier))
    #                 prefix = f"ingredient_{identifier}"
    #             except CocktailIngredient.DoesNotExist:
    #                 continue
    #         else:  # new
    #             ingredient = CocktailIngredient(cocktail=cocktail)
    #             prefix = f"ingredient_{identifier}"
            
    #         ingredient_form = CocktailIngredientForm(
    #             request.POST,
    #             instance=ingredient,
    #             prefix=prefix
    #         )
    #         ingredient_forms.append(ingredient_form)
    #         if not ingredient_form.is_valid():
    #             valid = False
    #             print(f"Form errors for {identifier}: {ingredient_form.errors}")  # Debug print

    #     if valid:
    #         cocktail = cocktail_form.save()
            
    #         # Delete ingredients that were removed
    #         ingredients_to_delete = existing_ingredient_ids - processed_ingredient_ids
    #         CocktailIngredient.objects.filter(
    #             id__in=ingredients_to_delete, 
    #             cocktail=cocktail
    #         ).delete()
            
    #         # Save all ingredient forms
    #         for ingredient_form in ingredient_forms:
    #             ingredient = ingredient_form.save(commit=False)
    #             ingredient.cocktail = cocktail
    #             ingredient.save()

    #         messages.success(request, f"The cocktail '{cocktail.name}' was successfully updated!")
    #         return redirect('cocktail-list')

    #     # If we get here, there were validation errors
    #     print("Form validation failed")  # Debug print
    #     for form in ingredient_forms:
    #         print(f"Form errors: {form.errors}")  # Debug print

    #     return render(request, 'cocktails/cocktail_edit.html', {
    #         'cocktail_form': cocktail_form,
    #         'ingredient_forms': ingredient_forms,
    #     })
    
class CocktailListView(ListView):
    model = Cocktail
    context_object_name = 'cocktails'
    template_name = 'cocktails/cocktail_list.html'

    def get_queryset(self):
        # Sort the ingredients alphabetically by name
        return Cocktail.objects.all().order_by("name")

class CocktailDetailView(DetailView):
    model = Cocktail
    context_object_name = 'cocktail'
    template_name = 'cocktails/cocktail_details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Prefetch the ingredient relation to include the brand
        cocktail_ingredients = CocktailIngredient.objects.filter(cocktail=self.object).select_related('ingredient')
        
        # Add ingredients to context with brand details
        context['cocktail_ingredients'] = [
            {
                'ingredient': ci.ingredient, 
                'quantity': ci.quantity, 
                'unit': ci.get_unit_display(),
                'brand': ci.ingredient.brand  if ci.ingredient else "No brand available"  # Handle None case
            }
            for ci in cocktail_ingredients
        ]
        return context
    
class ConfirmCocktailDeleteView(DetailView):
    def get(self, request, pk):
        cocktail = get_object_or_404(Cocktail, pk=pk)
        return render(request, 'cocktails/partials/cocktail_confirm_delete.html', {'cocktail': cocktail})

    def post(self, request, pk):
        cocktail = get_object_or_404(Cocktail, pk=pk)
        cocktail.delete()
        messages.success(request, f"The cocktail '{cocktail.name}' was successfully deleted!")
        return redirect('cocktail-list')

class DeleteCocktailView(TemplateView):
    def get(self, request, pk):
        cocktail = get_object_or_404(Cocktail, pk=pk)
        return render(request, 'cocktails/partials/cocktail_delete.html', {'cocktail': cocktail})

    def post(self, request, pk):
        cocktail = get_object_or_404(Cocktail, pk=pk)
        cocktail.delete()
        messages.success(request, f"The cocktail '{cocktail.name}' was successfully deleted!")
        return redirect('cocktail-list')

class SelectIngredientsView(FormView):
    template_name = "cocktails/select_ingredients.html"
    form_class = SelectIngredientsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cocktail = get_object_or_404(Cocktail, pk=self.kwargs["pk"])
        context["cocktail"] = cocktail
        # Pass pre-selected ingredient IDs to the template
        context["selected_ingredient_ids"] = list(cocktail.ingredients.values_list("ingredient_id", flat=True))
        return context

    def get_form(self):
        """Override to pre-select ingredients already associated with the cocktail."""
        form = super().get_form()
        cocktail = get_object_or_404(Cocktail, pk=self.kwargs["pk"])

        # Pre-select ingredients associated with the cocktail
        selected_ingredients = cocktail.ingredients.values_list("ingredient_id", flat=True)
        form.fields["ingredients"].initial = Ingredient.objects.filter(id__in=selected_ingredients)
        return form

    def form_valid(self, form):
        cocktail = get_object_or_404(Cocktail, pk=self.kwargs["pk"])
        selected_ingredients = form.cleaned_data["ingredients"]

        # Sync cocktail's ingredients with the selected ones
        # Remove ingredients no longer selected
        CocktailIngredient.objects.filter(cocktail=cocktail).exclude(
            ingredient__in=selected_ingredients
        ).delete()

        # Add or update new ingredients
        for ingredient in selected_ingredients:
            CocktailIngredient.objects.get_or_create(
                cocktail=cocktail,
                ingredient=ingredient,
                defaults={"quantity": 0, "unit": "ounce"},  # Adjust defaults as needed
            )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cocktail-list")  # Adjust to your detail view

    
class CocktailIngredientOptions(TemplateView):

    def get(self, request):
        ingredient_form = CocktailIngredientForm()
        return render(request, 'cocktails/partials/ingredient_form_component.html', {
            'ingredient_form': ingredient_form,
        })