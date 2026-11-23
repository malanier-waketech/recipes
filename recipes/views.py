from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CommentForm, RecipeIngredientFormSet
from .models import Recipe

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
