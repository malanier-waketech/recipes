from django.contrib import admin

from .models import Category, Ingredient, Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    """Allow ingredients to be added directly to a recipe."""

    model = RecipeIngredient
    extra = 3
    autocomplete_fields = ["ingredient"]
    fields = ["ingredient", "quantity", "unit"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Customize the recipe administration page."""

    list_display = [
        "title",
        "owner_id",
        "category",
        "difficulty",
        "prep_time",
        "cook_time",
        "is_favorite",
        "created_at",
    ]

    list_filter = [
        "category",
        "difficulty",
        "is_favorite",
        "created_at",
    ]

    search_fields = [
        "title",
        "description",
        "owner_id__username",
    ]

    inlines = [RecipeIngredientInline]

    fieldsets = (
        (
            "Recipe Information",
            {
                "fields": (
                    "title",
                    "description",
                    "instructions",
                )
            },
        ),
        (
            "Recipe Details",
            {
                "fields": (
                    ("prep_time", "cook_time"),
                    ("servings", "difficulty"),
                    "category",
                    "owner_id",
                    "is_favorite",
                )
            },
        ),
        (
            "External Recipe Information",
            {
                "fields": (
                    "source_name",
                    "source_id",
                    "source_url",
                    "image_url",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Manage ingredients."""

    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Manage recipe categories."""

    list_display = ["name"]
    search_fields = ["name"]
