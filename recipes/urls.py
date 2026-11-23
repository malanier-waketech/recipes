from django.urls import path

from .views import (
    RecipeCreateView,
    RecipeDeleteView,
    RecipeDetailView,
    RecipeListView,
    RecipeUpdateView,
    recipe_api_import,
    recipe_api_search,
)

urlpatterns = [
    path("<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("<int:pk>/edit/", RecipeUpdateView.as_view(), name="recipe_edit"),
    path("<int:pk>/delete/", RecipeDeleteView.as_view(), name="recipe_delete"),
    path("new/", RecipeCreateView.as_view(), name="recipe_new"),
    path("", RecipeListView.as_view(), name="recipe_list"),
    path("find/", recipe_api_search, name="recipe_api_search"),
    path("import/<str:meal_id>/", recipe_api_import, name="recipe_api_import"),
]
