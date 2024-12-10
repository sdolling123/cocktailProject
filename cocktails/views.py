from django.shortcuts import render, redirect, get_object_or_404
from formtools.wizard.views import SessionWizardView
from .models import Cocktail, CocktailIngredient
from .forms import CocktailBasicDetailsForm, CocktailIngredientsForm, CocktailInstructionsForm, PlaceholderForm, SelectIngredientsForm, AddIngredientDetailsForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from ingredients.models import Ingredient
from django.forms import formset_factory

# Create your views here.
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
        context['cocktail_ingredients'] = CocktailIngredient.objects.filter(cocktail = self.object)
        return context

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

class CocktailWizardView(SessionWizardView):
    form_list = [
        ("step1", CocktailBasicDetailsForm),
        ("step2", SelectIngredientsForm),
        ("step3", AddIngredientDetailsForm),
        ("step4", CocktailInstructionsForm),
    ]
    TEMPLATES = {
        "step1": "cocktails/step1_basic_details.html",
        "step2": "cocktails/select_ingredients.html",
        "step3": "cocktails/step3_ingredient_details.html",
        "step4": "cocktails/step4_instructions.html",
    }

    def get_template_names(self):
        """
        Used to provide the template for a given step in the process
        """
        return [self.TEMPLATES[self.steps.current]]

    def get_form(self, step=None, data=None, files=None):
        if step is None:
            step = self.steps.current

        # Special handling for step 3
        if step == "step3":
            # Get selected ingredients from step 2
            step2_data = self.storage.data.get("step_data", {}).get("step2", {})
            selected_ingredient_ids = step2_data.get("ingredients", [])
            print(selected_ingredient_ids)
            
            # If we're on step 3, create multiple forms based on selected ingredients
            if selected_ingredient_ids:
                # Retrieve previous step 3 data from session if exists
                previous_step3_data = self.storage.data.get("step_data", {}).get("step3", {})
                
                # Dynamically generate forms for each selected ingredient
                form_class = formset_factory(
                    AddIngredientDetailsForm, 
                    extra=0,
                    min_num=len(selected_ingredient_ids)
                )
                
                # Prepare initial data
                initial = []
                for ingredient_id in selected_ingredient_ids:
                    # Try to get previously entered data for this ingredient
                    ingredient_data = previous_step3_data.get(str(ingredient_id), {})
                    initial.append(ingredient_data)
                
                # If data is provided, use it, otherwise use initial
                if data:
                    return form_class(data, initial=initial)
                return form_class(initial=initial)
        
        # For other steps, use default form creation
        return super().get_form(step, data, files)
    
    def get_context_data(self, form, **kwargs):
        """
        Adds custom data to the template context.
        Called each time a step's form is rendered.
        """
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == "step2":
            # Retrieve step 2 data
            step2_data = self.storage.data.get("step_data", {}).get("step2", {})
            context["selected_ingredient_ids"] = step2_data.get("ingredients", []) if step2_data else []

        if self.steps.current == "step3":
            # Get selected ingredients to pass to template
            step2_data = self.storage.data.get("step_data", {}).get("step2", {})
            selected_ingredient_ids = step2_data.get("ingredients", [])
            
            # Create a dictionary of ingredients keyed by their index
            ingredients_dict = {
                i: ingredient.name 
                for i, ingredient in enumerate(Ingredient.objects.filter(id__in=selected_ingredient_ids))
        }
        
            print(ingredients_dict)
            context['ingredients'] = ingredients_dict

        return context
    
    def process_step(self, form):
        """
        Processes and stores data from the current step.
        After the user submits a step's form.
        """
        step_data = super().process_step(form)

        if self.steps.current == "step2":
            step2_data = self.storage.data.get("step_data", {}).get("step2", {})
            ingredient_ids = step2_data.get("ingredients", [])
            step2_data["ingredients"] = ingredient_ids  # Convert QuerySet to list

        if self.steps.current == "step3":
            step2_data = self.storage.data.get("step_data", {}).get("step2", {})
            selected_ingredient_ids = step2_data.get("ingredients", [])

            # Prepare step3 data
            step3_data = {}
            for form_instance, ingredient_id in zip(form.forms, selected_ingredient_ids):
                if form_instance.is_valid():
                    ingredient_data = form_instance.cleaned_data
                    step3_data[str(ingredient_id)] = {
                        'quantity': ingredient_data.get('quantity', 0),
                        'unit': ingredient_data.get('unit', 'ounce')
                    }

            # Store the processed data explicitly
            self.storage.data["step_data"]["step3_processed"] = step3_data
        
        return super().process_step(form)

        # return step_data

    def done(self, form_list, **kwargs):
        step1_data = self.get_cleaned_data_for_step("step1")
        # step3_data = self.get_cleaned_data_for_step("step3")
        # print("clean data in done",step3_data)
        step4_data = self.get_cleaned_data_for_step("step4")

        # Ensure step3_data is a dictionary
        step3_data = self.storage.data.get("step_data", {}).get("step3_processed", {})
        print("Processed step3_data in done:", step3_data)
        # if not isinstance(step3_data, dict):
        #     step3_data = {}

        step2_data = self.storage.data.get("step_data", {}).get("step2", {})
        ingredient_ids = step2_data.get("ingredients", [])
        ingredients = Ingredient.objects.filter(id__in=ingredient_ids)

        # Create or update the cocktail only at the end
        cocktail, _ = Cocktail.objects.update_or_create(
            name=step1_data["name"],
            defaults={"type": step1_data["type"], "style": step1_data["style"]},
        )

        # Sync ingredients
        selected_ingredients = step2_data["ingredients"]
        CocktailIngredient.objects.filter(cocktail=cocktail).exclude(
            ingredient__in=selected_ingredients).delete()

        # Example: Loop through the data and handle it
        for ingredient_id, details in step3_data.items():
            print("ingredient_id: ", ingredient_id)
            print("details: ", details)
            quantity = details.get("quantity", 0)
            unit = details.get("unit", "unknown")

            # Example operation: Look up the ingredient and perform an action
            ingredient = Ingredient.objects.get(id=ingredient_id)
            print(f"Ingredient: {ingredient.name}, Quantity: {quantity}, Unit: {unit}")

            # Add or update ingredient details (e.g., create a CocktailIngredient record)
            CocktailIngredient.objects.update_or_create(
                cocktail=cocktail,
                ingredient=ingredient,
                quantity=quantity,
                unit=unit,
            )

        # Save instructions
        cocktail.instructions = step4_data["instructions"]
        cocktail.save()

        return redirect(reverse_lazy("cocktail-list"))