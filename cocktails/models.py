from django.db import models
from ingredients.models import Ingredient

# Create your models here.
class Cocktail(models.Model):
    COCKTAIL_TYPES = [
        ('shaken', 'Shaken'),
        ('stirred', 'Stirred'),
        ('built', 'Built'),
        ('frozen', 'Frozen'),
        ('blended', 'Blended'),
    ]

    STYLE_CHOICES = [
        ('tiki', 'Tiki'),
        ('modern', 'Modern'),
        ('sour', 'Sour'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=COCKTAIL_TYPES)
    style = models.CharField(max_length=10, choices=STYLE_CHOICES)
    instructions = models.TextField()
    creator = models.CharField(max_length=100, blank=True, null=True)  # New field

    def __str__(self):
        return self.name

class CocktailIngredient(models.Model):
    cocktail = models.ForeignKey(Cocktail, related_name='ingredients', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20, choices=[
        ('slice', 'Slice'),
        ('wedge', 'Wedge'),
        ('drop', 'Drop'),
        ('dash', 'Dash'),
        ('millimeter', 'Millimeter'),
        ('ounce', 'Ounce'),
        ('cup', 'Cup'),
    ])
    
    def get_abbreviated_unit(self):
        abbreviations = {
            'millimeter': 'ml',
            'ounce': 'oz',
            'cup': 'c',
        }
        # Return the abbreviation if available; otherwise, return the full unit name
        return abbreviations.get(self.unit, self.unit)

    def __str__(self):
        return f'{self.quantity} {self.unit} of {self.ingredient.name}'