"""
heuristic.py
============
Heuristic cost function for the meal plan search.

The cost function measures how far the current meal plan totals are
from the user's daily nutritional targets. Lower cost = better plan.

This mirrors the concept of an admissible heuristic in A* search —
it never overestimates the true remaining cost.
"""


# Daily nutritional targets per health condition
# Format: {calories (kcal), protein (g), carbs (g), fat (g)}
DAILY_TARGETS = {
    "diabetic":     {"calories": 1500, "protein": 85,  "carbs": 120, "fat": 50},
    "weight_loss":  {"calories": 1300, "protein": 80,  "carbs": 140, "fat": 40},
    "high_protein": {"calories": 2100, "protein": 140, "carbs": 200, "fat": 65},
    "low_fat":      {"calories": 1600, "protein": 80,  "carbs": 220, "fat": 35},
    "vegetarian":   {"calories": 1700, "protein": 70,  "carbs": 220, "fat": 55},
    "general":      {"calories": 1800, "protein": 75,  "carbs": 230, "fat": 60},
}

# Nutrient weights — how much each nutrient deviation is penalised
# Protein is weighted 2x because meeting protein targets is harder
WEIGHTS = {
    "calories": 1.0,
    "protein":  2.0,
    "carbs":    1.0,
    "fat":      1.5,
}


def heuristic_cost(current_totals: dict, targets: dict) -> float:
    """
    Weighted Manhattan distance between current plan totals and daily targets.

    Formula:
        cost = Σ weight_n × |current_n - target_n|   for each nutrient n

    Args:
        current_totals: dict with keys calories, protein, carbs, fat
        targets:        dict with the same keys (daily goals)

    Returns:
        float — lower is better
    """
    cost = 0.0
    for nutrient, weight in WEIGHTS.items():
        cost += weight * abs(current_totals[nutrient] - targets[nutrient])
    return cost


def get_targets(condition: str) -> dict:
    """Return the daily nutritional targets for a given health condition."""
    return DAILY_TARGETS.get(condition, DAILY_TARGETS["general"])
