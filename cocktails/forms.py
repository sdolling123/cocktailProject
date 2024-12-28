from django import forms
from .models import Cocktail, CocktailIngredient
from ingredients.models import Ingredient
from django.forms import formset_factory
import uuid

class CocktailBasicDetailsForm(forms.ModelForm):
    class Meta:
        model = Cocktail
        fields = ['name', 'creator', 'type', 'style']

class CocktailIngredientsForm(forms.Form):
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), widget=forms.CheckboxSelectMultiple)
    quantity = forms.FloatField(min_value=0)
    unit = forms.ChoiceField(choices=[('slice', 'Slice'), ('wedge', 'Wedge'), ('drop', 'Drop'), ('dash', 'Dash'),
                                     ('milliliter', 'Milliliter'), ('ounce', 'Ounce'), ('cup', 'Cup')])

    def save(self, cocktail):
        for ingredient in self.cleaned_data['ingredients']:
            CocktailIngredient.objects.create(
                cocktail=cocktail,
                ingredient=ingredient,
                quantity=self.cleaned_data['quantity'],
                unit=self.cleaned_data['unit']
            )
    
class CocktailInstructionsForm(forms.Form):
    instructions = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False,)
    
class PlaceholderForm(forms.Form):
    pass

class SelectIngredientsForm(forms.Form):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'ingredient-checkbox'}),
        label="Select Ingredients",
        required=False,
    )
    
    def get_ingredient_details(self):
        # Return a dictionary with ingredient id as key and additional details as value
        return {ingredient.id: ingredient for ingredient in self.fields['ingredients'].queryset}
    
class AddIngredientDetailsForm(forms.Form):
    quantity = forms.FloatField(min_value=0, required=False)
    unit = forms.ChoiceField(
        choices=[('Drop','drop'), ('Dash', 'dash'), ('Slice', 'slice'), ('Wedge', 'wedge'), 
                  ('Milliliter', 'ml'), ('Ounce', 'oz'), ('Cup', 'c')],
        required=False,
        initial='Milliliter',
    )
    
class CocktailForm(forms.ModelForm):
    class Meta:
        model = Cocktail
        fields = ['name', 'creator', 'type', 'style', 'instructions']
        
    name = forms.CharField(label="Name",label_suffix=":",help_text="This is a required field.",error_messages={"required":"Please fill this out"})
    instructions = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False,)

class CocktailIngredientForm(forms.ModelForm):
    class Meta:
        model = CocktailIngredient
        fields = ['ingredient', 'quantity', 'unit']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unique_id = uuid.uuid4().hex  # Generate a unique ID for this form instance
        self.fields['ingredient'].widget.attrs.update({
            'class': 'hidden',
            'id': f'ingredient_id_{unique_id}'
        })
        self.fields['quantity'].widget.attrs.update({
            # 'class': 'select-as-input',
            'id': f'ingredient_quantity_{unique_id}'
        })
        self.fields['unit'].widget.attrs.update({
            # 'class': 'select-as-input',
            'id': f'ingredient_unit_{unique_id}'
        })
    
    # Define the 'ingredient' field as a Select field
    # ingredient = forms.ModelChoiceField(
    #     queryset=Ingredient.objects.all(),
    #     widget=forms.Select(attrs={'class': 'select-as-input', 'id':f'ingredient_name_{unique_id}'}),  # Add a class for styling/identification
    #     required=False,
    # )

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        ingredient = cleaned_data.get('ingredient')

        # If quantity is provided, ingredient must also be provided
        if quantity and not ingredient:
            self.add_error('ingredient', "Ingredient is required if quantity is provided.")

        return cleaned_data