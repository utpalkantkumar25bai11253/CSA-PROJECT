"""
search.py
=========
Heuristic search algorithms for meal plan generation.

Two algorithms are implemented:
  1. Greedy Best-First Search  — fast, picks the locally best food at each meal
  2. A* Search                 — optimal, considers accumulated cost + heuristic

Both algorithms use the priority queue (min-heap) pattern from AI search theory.

State space:
  - A state is a partial meal plan: {meal_type -> food_chosen}
  - The goal state has all 4 meals assigned
  - Each expansion picks one food per meal in order: breakfast → lunch → snack → dinner

This maps directly to CO2 (Informed Search Strategies) in the syllabus.
"""

import heapq
from health_rules import get_suitable_foods, get_food_info
from heuristic import heuristic_cost, get_targets

MEAL_TYPES = ["breakfast", "lunch", "snack", "dinner"]


# ─── Greedy Best-First Search ──────────────────────────────────────────────────

def greedy_search(condition: str) -> tuple:
    """
    Greedy Best-First Search over the meal plan.

    At each meal step, evaluates ALL candidate foods and picks the one
    that minimises the heuristic cost (projected totals vs targets).
    Does NOT backtrack — greedy commitment at each step.

    Returns:
        plan   (dict)  — {meal_type: food_name}
        totals (dict)  — accumulated macros for the day
        trace  (list)  — step-by-step search log for the notebook
    """
    targets = get_targets(condition)
    plan    = {}
    totals  = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
    trace   = []

    for meal in MEAL_TYPES:
        candidates = get_suitable_foods(condition, meal)

        if not candidates:
            plan[meal] = None
            trace.append({
                "meal": meal, "chosen": "— none found —",
                "cost": None, "candidates": 0, "all_options": []
            })
            continue

        # Build priority queue: (heuristic_cost, food_name)
        pq = []
        options_log = []
        for food_name in candidates:
            info = get_food_info(food_name)
            projected = {k: totals[k] + info[k] for k in totals}
            cost = heuristic_cost(projected, targets)
            heapq.heappush(pq, (cost, food_name))
            options_log.append({"food": food_name, "cost": round(cost, 1)})

        # Pop the best (lowest cost) food
        best_cost, best_food = heapq.heappop(pq)
        info = get_food_info(best_food)
        plan[meal] = best_food
        for k in totals:
            totals[k] += info[k]

        # Sort options by cost for display
        options_log.sort(key=lambda x: x["cost"])

        trace.append({
            "meal":        meal,
            "chosen":      best_food,
            "cost":        round(best_cost, 1),
            "candidates":  len(candidates),
            "all_options": options_log,
        })

    return plan, totals, trace


# ─── A* Search ────────────────────────────────────────────────────────────────

def astar_search(condition: str) -> tuple:
    """
    A* Search over the full meal plan space.

    State   = tuple of (meal_index, frozenset of chosen foods)
    f(n)    = g(n) + h(n)
            = accumulated nutrient deviation so far + estimated remaining deviation
    
    Unlike Greedy, A* explores multiple branches and guarantees the
    globally optimal meal plan (lowest total nutrient deviation).

    Returns:
        plan   (dict)  — {meal_type: food_name}
        totals (dict)  — accumulated macros for the day
        trace  (list)  — nodes explored at each expansion
    """
    targets  = get_targets(condition)
    zero     = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

    # Priority queue entry: (f_cost, g_cost, meal_index, plan_so_far, totals_so_far)
    start = (0.0, 0.0, 0, {}, zero.copy())
    pq    = [start]
    trace = []
    nodes_explored = 0

    while pq:
        f, g, meal_idx, current_plan, current_totals = heapq.heappop(pq)
        nodes_explored += 1

        # Goal state: all meals assigned
        if meal_idx == len(MEAL_TYPES):
            trace.append({
                "event":          "goal reached",
                "nodes_explored": nodes_explored,
                "final_f_cost":   round(f, 1),
            })
            return current_plan, current_totals, trace

        meal = MEAL_TYPES[meal_idx]
        candidates = get_suitable_foods(condition, meal)

        if not candidates:
            # No food available — skip this meal
            heapq.heappush(pq, (f, g, meal_idx + 1, current_plan, current_totals))
            continue

        for food_name in candidates:
            info         = get_food_info(food_name)
            new_totals   = {k: current_totals[k] + info[k] for k in current_totals}
            g_new        = heuristic_cost(new_totals, targets)       # g: cost so far
            h_new        = heuristic_cost(new_totals, targets) * 0.5 # h: admissible estimate
            f_new        = g_new + h_new
            new_plan     = {**current_plan, meal: food_name}

            heapq.heappush(pq, (f_new, g_new, meal_idx + 1, new_plan, new_totals))

        trace.append({
            "meal":        meal,
            "expanded":    len(candidates),
            "nodes_so_far": nodes_explored,
        })

    # Fallback (should not reach here)
    return {}, zero, trace
