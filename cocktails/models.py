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

    def __str__(self):
        return f'{self.quantity} {self.unit} of {self.ingredient.name}'