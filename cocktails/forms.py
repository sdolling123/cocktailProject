from django import forms
from .models import Cocktail, CocktailIngredient
from ingredients.models import Ingredient

class CocktailBasicDetailsForm(forms.ModelForm):
    class Meta:
        model = Cocktail
        fields = ['name', 'type', 'style']

class CocktailIngredientsForm(forms.Form):
    ingredients = forms.ModelMultipleChoiceField(
    queryset=Ingredient.objects.all(),
    widget=forms.SelectMultiple,  # Use dropdown for multiple selections
    label="Select Ingredients"
    )
    quantity = forms.FloatField(min_value=0, label="Quantity")
    unit = forms.ChoiceField(choices=[('slice', 'Slice'), ('wedge', 'Wedge'), ('drop', 'Drop'), ('dash', 'Dash'),
                                     ('millimeter', 'Millimeter'), ('ounce', 'Ounce'), ('cup', 'Cup')],
                             label="Unit")
    
class CocktailInstructionsForm(forms.Form):
    instructions = forms.CharField(widget=forms.Textarea)