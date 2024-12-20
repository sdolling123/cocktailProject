# Generated by Django 5.1.3 on 2024-11-24 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ingredient_type', models.CharField(choices=[('spirit', 'Spirit'), ('modified_spirit', 'Modified Spirit'), ('citrus', 'Citrus'), ('bitters', 'Bitters'), ('liqueur', 'Liqueur'), ('sweetener', 'Sweetener'), ('fruit_puree', 'Fruit/Puree'), ('herb_spice', 'Herb/Spice'), ('garnish', 'Garnish'), ('dairy_cream', 'Dairy/Cream'), ('syrup_flavoring', 'Syrup/Flavoring'), ('vegetable', 'Vegetable'), ('wine_fortified_wine', 'Wine/Fortified Wine'), ('extract', 'Extract'), ('ice', 'Ice')], max_length=20)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('abv', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Alcohol by Volume (%)')),
                ('sweetness', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Sweetness (%)')),
                ('acid', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Acid (%)')),
                ('instructions', models.TextField(blank=True, null=True, verbose_name='How to create')),
            ],
        ),
    ]
