from django import forms
from .models import Cocktail, CocktailIngredient
from ingredients.models import Ingredient

class CocktailBasicDetailsForm(forms.ModelForm):
    class Meta:
        model = Cocktail
        fields = ['name', 'type', 'style']

class CocktailIngredientsForm(forms.Form):
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), widget=forms.CheckboxSelectMultiple)
    quantity = forms.FloatField(min_value=0)
    unit = forms.ChoiceField(choices=[('slice', 'Slice'), ('wedge', 'Wedge'), ('drop', 'Drop'), ('dash', 'Dash'),
                                     ('millimeter', 'Millimeter'), ('ounce', 'Ounce'), ('cup', 'Cup')])

    def save(self, cocktail):
        for ingredient in self.cleaned_data['ingredients']:
            CocktailIngredient.objects.create(
                cocktail=cocktail,
                ingredient=ingredient,
                quantity=self.cleaned_data['quantity'],
                unit=self.cleaned_data['unit']
            )
    
class CocktailInstructionsForm(forms.Form):
    instructions = forms.CharField(widget=forms.Textarea)
    
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