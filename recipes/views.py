from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView

from .models import Recipe


# Create your views here.
class RecipeListView(ListView):
    model = Recipe
    template_name = "recipe_list.html"


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipe_detail.html"


class RecipeUpdateView(UpdateView):
    model = Recipe
    fields = (
        "title",
        "description",
        "instructions",
        "prep_time",
        "cook_time",
        "servings",
        "difficulty",
        "category",
    )
    template_name = "recipe_edit.html"


class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = "recipe_delete.html"
    success_url = reverse_lazy("recipe_list")
