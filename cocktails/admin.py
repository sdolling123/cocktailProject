from django.contrib import admin
from cocktails.models import Cocktail,CocktailIngredient

# Register your models here.
class CocktailAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    
class CocktailIngredientAdmin(admin.ModelAdmin):
    list_display = ('id','ingredient','cocktail')
    
    
admin.site.register(Cocktail, CocktailAdmin)
admin.site.register(CocktailIngredient, CocktailIngredientAdmin)
