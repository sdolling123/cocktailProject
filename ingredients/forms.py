from django import forms
from .models import Ingredient

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name',
                  'ingredient_type',
                  'brand',
                  'abv',
                  'sweetness',
                  'acid',
                  'instructions']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 4}),
        }