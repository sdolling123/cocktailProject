from django.db import models

# Create your models here.
class Ingredient(models.Model):
    TYPE_CHOICES = [
        ('spirit', 'Spirit'),
        ('modified_spirit', 'Modified Spirit'),
        ('citrus', 'Citrus'),
        ('bitters', 'Bitters'),
        ('liqueur', 'Liqueur'),
        ('sweetener', 'Sweetener'),
        ('fruit_puree', 'Fruit/Puree'),
        ('herb_spice', 'Herb/Spice'),
        ('garnish', 'Garnish'),
        ('dairy_cream', 'Dairy/Cream'),
        ('syrup_flavoring', 'Syrup/Flavoring'),
        ('vegetable', 'Vegetable'),
        ('wine_fortified_wine', 'Wine/Fortified Wine'),
        ('extract', 'Extract'),
        ('ice', 'Ice'),
    ]

    name = models.CharField(max_length=100)
    ingredient_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    brand = models.CharField(max_length=100, blank=True, null=True)
    abv = models.DecimalField("Alcohol by Volume (%)", max_digits=5, decimal_places=2, blank=True, null=True)
    sweetness = models.DecimalField("Sweetness (%)", max_digits=5, decimal_places=2, blank=True, null=True)
    acid = models.DecimalField("Acid (%)", max_digits=5, decimal_places=2, blank=True, null=True)
    instructions = models.TextField("How to create", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.ingredient_type})"