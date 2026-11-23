from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    """Stores recipe categories created by users."""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories"
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Stores ingredients that can be used in recipes."""

    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Stores recipes created or imported by users."""

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_favorite = models.BooleanField(default=False)

    # Recipe and ingredient relationship
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient", related_name="recipes"
    )
    instructions = models.TextField()
    prep_time = models.PositiveIntegerField(
        default=0, help_text="Preparation time in minutes"
    )
    cook_time = models.PositiveIntegerField(
        default=0, help_text="Cooking time in minutes"
    )
    servings = models.PositiveIntegerField(default=1)
    difficulty = models.CharField(
        max_length=10, choices=DIFFICULTY_CHOICES, default="easy"
    )

    owner_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipes"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recipes",
    )

    # External recipe source information
    source_name = models.CharField(max_length=100, blank=True)
    source_id = models.CharField(max_length=100, blank=True)
    source_url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.pk})

    @property
    def total_time(self):
        """Return total preparation and cooking time."""
        return self.prep_time + self.cook_time

    # External API information
    themealdb_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_index=True,
    )

    image_url = models.URLField(
        max_length=500,
        blank=True,
    )

    source_url = models.URLField(
        max_length=500,
        blank=True,
    )


class RecipeIngredient(models.Model):
    """Links ingredients to recipes with measurements."""

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    quantity = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    unit = models.CharField(max_length=50, blank=True)

    measurement = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Quantity and unit, such as 2 cups or 1 tbsp.",
    )

    def __str__(self):
        """Display ingredient with its measurement."""

        measurement = self.measurement.strip()

        if not measurement:
            quantity = str(self.quantity) if self.quantity is not None else ""
            measurement = f"{quantity} {self.unit}".strip()

        return f"{measurement} {self.ingredient.name}".strip()


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    comment = models.CharField(max_length=140)
    owner_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse("recipe_list")
