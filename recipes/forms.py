from django import forms
from django.forms import inlineformset_factory

from .models import Comment, Recipe, RecipeIngredient

RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    fields=[
        "ingredient",
        "quantity",
        "unit",
    ],
    extra=3,
    can_delete=True,
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {
            "comment",
        }
