import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen
from django.conf import settings

BASE_URL = (
    "https://www.themealdb.com/api/json/v1/"
    f"{getattr(settings, 'THEMEALDB_API_KEY', '1')}"
)


class MealDBError(Exception):
    """Raised when TheMealDB cannot be accessed."""


def fetch_meals(endpoint, params):
    """Make a server-side request to TheMealDB."""

    try:
        url = f"{BASE_URL}/{endpoint}?{urlencode(params)}"
        with urlopen(url, timeout=10) as response:
            data = json.loads(response.read())

        if not isinstance(data, dict):
            raise MealDBError("Invalid API response.")

        return data.get("meals") or []

    except (URLError, TimeoutError, ValueError) as exc:
        raise MealDBError(
            "Unable to retrieve recipes from TheMealDB."
        ) from exc


def search_meals(query):
    """Search meals by name."""

    return fetch_meals(
        "search.php",
        {"s": query},
    )


def get_meal(meal_id):
    """Retrieve one meal by its API ID."""

    meals = fetch_meals(
        "lookup.php",
        {"i": meal_id},
    )

    return meals[0] if meals else None


def extract_ingredients(meal):
    """Convert API ingredient fields into a list."""

    ingredients = []

    for number in range(1, 21):
        name = (
            meal.get(f"strIngredient{number}") or ""
        ).strip()

        measurement = (
            meal.get(f"strMeasure{number}") or ""
        ).strip()

        if name:
            ingredients.append({
                "name": name,
                "measurement": measurement,
            })

    return ingredients