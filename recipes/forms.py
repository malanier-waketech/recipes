from django.forms import inlineformset_factory

from .models import Recipe, RecipeIngredient

RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    fields=["ingredient", "quantity", "unit"],
    extra=3,
    can_delete=True,
)
