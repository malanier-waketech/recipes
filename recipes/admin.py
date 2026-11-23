from django.contrib import admin

from .models import (
    Category,
    Comment,
    Ingredient,
    Recipe,
    RecipeIngredient,
)


# --------------------------------------------------
# INLINE ADMIN CLASSES
# --------------------------------------------------
class RecipeIngredientInline(admin.TabularInline):
    """Manage recipe ingredients directly within a recipe."""

    model = RecipeIngredient

    # Display three empty rows when adding a recipe.
    extra = 3

    # Allow searching for existing ingredients.
    autocomplete_fields = ["ingredient"]

    # Display all ingredient measurement fields.
    fields = [
        "ingredient",
        "quantity",
        "unit",
        "measurement",
    ]

    # Allow navigation to the ingredient relationship.
    show_change_link = True

    # Make ingredient rows removable.
    can_delete = True

    # Show existing rows plus three empty rows.
    max_num = 50


class CommentInline(admin.TabularInline):
    """Display comments within a recipe."""

    model = Comment
    extra = 0
    show_change_link = True


# --------------------------------------------------
# RECIPE ADMIN
# --------------------------------------------------


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Customize recipe management."""

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

    list_display_links = ["title"]

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

    list_per_page = 25

    ordering = ["-created_at"]

    # Display both ingredients and comments.
    inlines = [
        RecipeIngredientInline,
        CommentInline,
    ]

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
                    "themealdb_id",
                    "source_url",
                    "image_url",
                ),
                "classes": ("collapse",),
            },
        ),
    )


# --------------------------------------------------
# RECIPE INGREDIENT ADMIN
# --------------------------------------------------


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Manage recipe ingredient relationships."""

    list_display = [
        "recipe",
        "ingredient",
        "quantity",
        "unit",
        "measurement",
    ]

    list_filter = [
        "recipe",
        "ingredient",
    ]

    search_fields = [
        "recipe__title",
        "ingredient__name",
    ]

    autocomplete_fields = [
        "recipe",
        "ingredient",
    ]

    list_per_page = 25

    ordering = [
        "recipe__title",
        "ingredient__name",
    ]


# --------------------------------------------------
# INGREDIENT ADMIN
# --------------------------------------------------


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Manage ingredients."""

    list_display = ["name"]

    search_fields = ["name"]

    ordering = ["name"]

    list_per_page = 25


# --------------------------------------------------
# CATEGORY ADMIN
# --------------------------------------------------


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Manage recipe categories."""

    list_display = ["name"]

    search_fields = ["name"]

    ordering = ["name"]


# --------------------------------------------------
# COMMENT ADMIN
# --------------------------------------------------


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Manage recipe comments."""

    list_display = ["recipe", "id"]

    search_fields = ["recipe__title"]

    list_filter = ["recipe"]

    list_per_page = 25
