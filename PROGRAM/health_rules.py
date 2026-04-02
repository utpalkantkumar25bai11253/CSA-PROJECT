"""
health_rules.py
===============
Rule-based suitability engine — replaces Prolog health_rules.pl + validator.pl

Each rule is a Python function that mirrors a Prolog predicate, e.g.:
  suitable(Food, diabetic) :- food(Food, _, _, Carbs, _, _), Carbs < 15.
becomes:
  def rule_diabetic(food): return food["carbs"] < 15
"""

from food_data import FOODS


# ─── Suitability rules (one function per health condition) ─────────────────────

SUITABILITY_RULES = {
    "diabetic": {
        "description": "Low carbohydrate diet (< 15g carbs per item)",
        "check": lambda f: f["carbs"] < 15,
    },
    "weight_loss": {
        "description": "Low calorie diet (< 150 kcal per item)",
        "check": lambda f: f["calories"] < 150,
    },
    "high_protein": {
        "description": "High protein diet (> 8g protein per item)",
        "check": lambda f: f["protein"] > 8,
    },
    "vegetarian": {
        "description": "Vegetarian foods only",
        "check": lambda f: "veg" in f["tags"],
    },
    "low_fat": {
        "description": "Low fat diet (< 5g fat per item)",
        "check": lambda f: f["fat"] < 5,
    },
    "general": {
        "description": "No restrictions — balanced diet",
        "check": lambda f: True,
    },
}


# ─── Violation rules — mirrors Prolog validator.pl ─────────────────────────────

VIOLATION_RULES = {
    "diabetic": [
        {"condition": lambda f: f["carbs"] >= 30,    "reason": "High carbohydrate content (>= 30g)"},
        {"condition": lambda f: "high_sugar" in f["tags"], "reason": "Flagged as high-sugar food"},
    ],
    "weight_loss": [
        {"condition": lambda f: f["calories"] >= 250, "reason": "High calorie food (>= 250 kcal)"},
        {"condition": lambda f: f["fat"] >= 15,       "reason": "High fat content (>= 15g)"},
    ],
    "high_protein": [
        {"condition": lambda f: f["protein"] < 3,    "reason": "Very low protein content (< 3g)"},
    ],
    "low_fat": [
        {"condition": lambda f: f["fat"] >= 15,      "reason": "High fat content (>= 15g)"},
    ],
    "vegetarian": [
        {"condition": lambda f: "non_veg" in f["tags"], "reason": "Non-vegetarian food"},
    ],
    "general": [],
}


# ─── Query functions (mirror Prolog query interface) ───────────────────────────

def is_suitable(food_name: str, condition: str) -> bool:
    """
    Mirrors: suitable(Food, Condition) Prolog predicate.
    Returns True if the food satisfies the condition's rule.
    """
    food = FOODS.get(food_name)
    if not food:
        return False
    rule = SUITABILITY_RULES.get(condition, SUITABILITY_RULES["general"])
    return rule["check"](food)


def is_meal_suitable(food_name: str, meal_type: str) -> bool:
    """
    Mirrors: meal_suitable(Food, MealType) Prolog predicate.
    Returns True if the food's tags include the meal type.
    """
    food = FOODS.get(food_name)
    if not food:
        return False
    return meal_type in food["tags"]


def get_suitable_foods(condition: str, meal_type: str) -> list:
    """
    Combined query: suitable(Food, Condition), meal_suitable(Food, MealType).
    Returns list of food names satisfying both predicates.
    """
    results = []
    for name, food in FOODS.items():
        if is_suitable(name, condition) and is_meal_suitable(name, meal_type):
            results.append(name)
    return results


def check_violations(food_name: str, condition: str) -> list:
    """
    Mirrors: violation(Food, Condition, Reason) Prolog predicate.
    Returns list of violation reason strings.
    """
    food = FOODS.get(food_name)
    if not food:
        return []
    rules = VIOLATION_RULES.get(condition, [])
    return [r["reason"] for r in rules if r["condition"](food)]


def get_food_info(food_name: str) -> dict:
    """Return full macro info for a food item."""
    food = FOODS.get(food_name)
    if not food:
        return {}
    return {"name": food_name, **food}
