# %% [markdown]
# # Diet and Nutrition Advisor
# ### CSA2001 — Fundamentals in AI and ML | Project 3
# **Techniques used:** Rule-based Knowledge Representation · Greedy Best-First Search · A\* Search
#
# ---

# %% [markdown]
# ## Cell 1 — Imports and user profile

# %%
import sys
sys.path.insert(0, ".")   # make sure local modules are found

from food_data   import FOODS
from health_rules import get_suitable_foods, check_violations, get_food_info, SUITABILITY_RULES
from heuristic   import get_targets, DAILY_TARGETS, heuristic_cost
from search      import greedy_search, astar_search
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── User profile ──────────────────────────────────────────────────────────────
CONDITION = "diabetic"    # change to: weight_loss | high_protein | low_fat | vegetarian | general
ALGORITHM = "greedy"      # change to: greedy | astar

print(f"Condition : {CONDITION}")
print(f"Algorithm : {ALGORITHM}")
print(f"Target    : {get_targets(CONDITION)}")


# %% [markdown]
# ## Cell 2 — Knowledge base overview

# %%
rows = []
for name, f in FOODS.items():
    rows.append({
        "Food":     name,
        "Calories": f["calories"],
        "Protein":  f["protein"],
        "Carbs":    f["carbs"],
        "Fat":      f["fat"],
        "Tags":     ", ".join(f["tags"][:3]),
    })

df_foods = pd.DataFrame(rows)
print(f"Total foods in knowledge base: {len(df_foods)}\n")
print(df_foods.to_string(index=False))


# %% [markdown]
# ## Cell 3 — Rule query (mirrors Prolog predicate)

# %%
print(f"Rule: suitable(Food, {CONDITION})")
print(f"Description: {SUITABILITY_RULES[CONDITION]['description']}\n")

query_rows = []
for meal in ["breakfast", "lunch", "snack", "dinner"]:
    foods = get_suitable_foods(CONDITION, meal)
    query_rows.append({"Meal": meal.capitalize(), "Suitable foods": ", ".join(foods) or "— none —", "Count": len(foods)})

df_query = pd.DataFrame(query_rows)
print(df_query.to_string(index=False))


# %% [markdown]
# ## Cell 4 — Run heuristic search

# %%
if ALGORITHM == "astar":
    plan, totals, trace = astar_search(CONDITION)
    algo_label = "A* Search"
else:
    plan, totals, trace = greedy_search(CONDITION)
    algo_label = "Greedy Best-First Search"

print(f"Algorithm: {algo_label}\n")
print("Recommended meal plan:")
for meal, food in plan.items():
    info = get_food_info(food) if food else {}
    cal  = info.get("calories", "—")
    prot = info.get("protein",  "—")
    print(f"  {meal.capitalize():<12}  {str(food):<20}  {cal} kcal  {prot}g protein")

print(f"\nDay totals : {totals}")
print(f"Targets    : {get_targets(CONDITION)}")


# %% [markdown]
# ## Cell 5 — Search trace

# %%
trace_rows = []
for step in trace:
    if "event" in step:
        trace_rows.append({
            "Meal": "GOAL",
            "Chosen food": "—",
            "Heuristic cost": step.get("final_f_cost", "—"),
            "Candidates explored": step.get("nodes_explored", "—"),
        })
    elif step.get("chosen") != "— none found —":
        trace_rows.append({
            "Meal":               step.get("meal", "").capitalize(),
            "Chosen food":        step.get("chosen", ""),
            "Heuristic cost":     step.get("cost", ""),
            "Candidates explored": step.get("candidates", step.get("expanded", "")),
        })

df_trace = pd.DataFrame(trace_rows)
print(f"Search Trace — {algo_label}\n")
print(df_trace.to_string(index=False))


# %% [markdown]
# ## Cell 6 — Prolog-style violation check

# %%
print("Violation Report (mirrors Prolog validator.pl)\n")
violation_rows = []
for meal, food_name in plan.items():
    if not food_name:
        continue
    violations = check_violations(food_name, CONDITION)
    violation_rows.append({
        "Meal":       meal.capitalize(),
        "Food":       food_name,
        "Status":     "FLAGGED" if violations else "PASS",
        "Violations": "; ".join(violations) if violations else "—",
    })

df_viol = pd.DataFrame(violation_rows)
print(df_viol.to_string(index=False))


# %% [markdown]
# ## Cell 7 — Nutrition bar chart

# %%
targets   = get_targets(CONDITION)
nutrients = ["calories", "protein", "carbs", "fat"]
labels    = ["Calories (kcal)", "Protein (g)", "Carbs (g)", "Fat (g)"]
actual    = [totals[n] for n in nutrients]
target_v  = [targets[n] for n in nutrients]

x = range(len(nutrients))
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle(
    f"Nutrition Advisor — {CONDITION.replace('_', ' ').title()} | {algo_label}",
    fontsize=13, fontweight="bold"
)

ax = axes[0]
ax.bar([i - 0.2 for i in x], actual,    width=0.38, label="Actual", color="#1D9E75", alpha=0.9)
ax.bar([i + 0.2 for i in x], target_v,  width=0.38, label="Target", color="#7F77DD", alpha=0.6)
ax.set_xticks(list(x)); ax.set_xticklabels(labels, rotation=12, ha="right")
ax.set_ylabel("Amount"); ax.set_title("Actual vs Target")
ax.legend(); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

pct    = [round(a / t * 100, 1) if t else 0 for a, t in zip(actual, target_v)]
colors = ["#1D9E75" if 80 <= p <= 120 else "#E24B4A" if p > 130 else "#EF9F27" for p in pct]
ax2 = axes[1]
bars = ax2.barh(labels, pct, color=colors, alpha=0.85)
ax2.axvline(100, color="#7F77DD", linestyle="--", linewidth=1.2)
ax2.axvspan(80, 120, alpha=0.07, color="#1D9E75")
ax2.set_xlabel("% of daily target"); ax2.set_title("Target Achievement (%)")
ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)
for bar, p in zip(bars, pct):
    ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
             f"{p}%", va="center", fontsize=9)

plt.tight_layout()
plt.savefig("nutrition_chart.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart saved as nutrition_chart.png")


# %% [markdown]
# ## Cell 8 — Algorithm comparison (Greedy vs A*)

# %%
print("Comparing Greedy BFS vs A*\n")
g_plan, g_totals, g_trace = greedy_search(CONDITION)
a_plan, a_totals, a_trace = astar_search(CONDITION)

targets = get_targets(CONDITION)
g_cost  = heuristic_cost(g_totals, targets)
a_cost  = heuristic_cost(a_totals, targets)
a_nodes = next((s["nodes_explored"] for s in a_trace if "nodes_explored" in s), len(a_trace))

comparison = []
for meal in ["breakfast", "lunch", "snack", "dinner"]:
    comparison.append({
        "Meal":         meal.capitalize(),
        "Greedy choice": g_plan.get(meal, "—"),
        "A* choice":     a_plan.get(meal, "—"),
        "Same?":        "yes" if g_plan.get(meal) == a_plan.get(meal) else "no",
    })

df_cmp = pd.DataFrame(comparison)
print(df_cmp.to_string(index=False))
print(f"\nGreedy final cost : {g_cost:.1f}")
print(f"A*     final cost : {a_cost:.1f}")
print(f"A* nodes explored : {a_nodes}")
