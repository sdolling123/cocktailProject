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