from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CommentForm, RecipeIngredientFormSet
from .models import Category, Ingredient, Recipe, RecipeIngredient
from .services.themealdb import (
    MealDBError,
    extract_ingredients,
    get_meal,
    search_meals,
)

# Create your views here.


class CommentPost(SingleObjectMixin, FormView):
    model = Recipe
    form_class = CommentForm
    template_name = "recipe_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.recipe = self.object
        comment.owner_id = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        recipe = self.object
        return reverse("recipe_detail", kwargs={"pk": recipe.pk})


class CommentGet(DetailView):
    model = Recipe
    template_name = "recipe_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm
        return context


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipe_list.html"


class RecipeDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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

    def test_func(self):
        obj = self.get_object()
        return obj.owner_id == self.request.user


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = "recipe_delete.html"
    success_url = reverse_lazy("recipe_list")

    def test_func(self):
        obj = self.get_object()
        return obj.owner_id == self.request.user


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = "recipe_new.html"

    fields = (
        "title",
        "description",
        "instructions",
        "prep_time",
        "cook_time",
        "servings",
        "difficulty",
        "category",
        "is_favorite",
    )

    success_url = reverse_lazy("recipe_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "ingredient_formset" not in context:
            context["ingredient_formset"] = RecipeIngredientFormSet(
                self.request.POST if self.request.method == "POST" else None
            )

        return context

    def form_valid(self, form):
        ingredient_formset = RecipeIngredientFormSet(self.request.POST)

        if not ingredient_formset.is_valid():
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    ingredient_formset=ingredient_formset,
                )
            )

        with transaction.atomic():
            form.instance.owner_id = self.request.user
            self.object = form.save()

            ingredient_formset.instance = self.object
            ingredient_formset.save()

        return redirect(self.get_success_url())


## Search View
@login_required
def recipe_api_search(request):
    """Search TheMealDB for recipes."""

    query = request.GET.get("q", "").strip()
    meals = []
    error = None

    if query:
        try:
            meals = search_meals(query)
        except MealDBError as exc:
            error = str(exc)

    return render(
        request,
        "recipe_api_search.html",
        {
            "query": query,
            "meals": meals,
            "error": error,
        },
    )


## Import View
@login_required
@require_POST
def recipe_api_import(request, meal_id):
    """Import a meal into the user's cookbook."""

    try:
        meal = get_meal(meal_id)
    except MealDBError as exc:
        messages.error(request, str(exc))
        return redirect("recipe_api_search")

    if not meal:
        messages.error(request, "Recipe not found.")
        return redirect("recipe_api_search")

    # Prevent duplicate imports for this user.
    existing = Recipe.objects.filter(
        owner_id=request.user,
        themealdb_id=meal_id,
    ).first()

    if existing:
        messages.info(request, "Recipe already imported.")
        return redirect(existing.get_absolute_url())

    with transaction.atomic():
        category_name = (meal.get("strCategory") or "Uncategorized").strip()

        category, created = Category.objects.get_or_create(
            name=category_name,
            owner_id=request.user,
        )

        recipe = Recipe.objects.create(
            title=meal.get("strMeal") or "Untitled Recipe",
            description=(
                f"Imported from TheMealDB - "
                f"{meal.get('strArea') or 'International'} cuisine"
            ),
            instructions=meal.get("strInstructions") or "",
            category=category,
            owner_id=request.user,
            difficulty="easy",
            prep_time=0,
            cook_time=0,
            servings=1,
            themealdb_id=meal_id,
            image_url=meal.get("strMealThumb") or "",
            source_url=meal.get("strSource") or "",
        )

        for item in extract_ingredients(meal):
            ingredient, created = Ingredient.objects.get_or_create(
                name=item["name"],
            )

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                measurement=item["measurement"],
            )

    messages.success(
        request,
        f"{recipe.title} was imported successfully!",
    )

    return redirect(recipe.get_absolute_url())
