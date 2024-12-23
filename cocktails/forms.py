from django import forms
from .models import Cocktail, CocktailIngredient
from ingredients.models import Ingredient
from django.forms import formset_factory

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
    
    ingredient = forms.ChoiceField(
        required=False,
        help_text="Required if quantity and unit have values")
    # unit = forms.ChoiceField()
        # widgets = {
        #     'ingredient': forms.Select(attrs={'class': 'form-control'}),
        #     'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': False}),
        #     'unit': forms.Select(attrs={'class': 'form-control', 'required': False}),
        # }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        ingredient = cleaned_data.get('ingredient')

        # If quantity is provided, ingredient must also be provided
        if quantity and not ingredient:
            self.add_error('ingredient', "Ingredient is required if quantity is provided.")

        return cleaned_data