"""
main.py
=======
Diet and Nutrition Advisor — complete demo with AI Model
=========================================================

Run this file directly to see the full system in action:
    python main.py

Or import individual components in a Jupyter notebook.

Covers syllabus outcomes:
  CO2  — Informed search (Greedy BFS + A*)
  CO4  — Problem analysis and AI design
  CO5  — Real-world AI application
  CO6  — Prolog-style rule encoding (implemented in Python)
  NEW  — Self-learning AI model for adaptive recommendations
"""

import sys
import textwrap

# Fix Unicode encoding issues on Windows
sys.stdout.reconfigure(encoding='utf-8')

from health_rules import (
    get_suitable_foods, check_violations,
    get_food_info, SUITABILITY_RULES
)
from heuristic import get_targets, DAILY_TARGETS
from search import greedy_search, astar_search
import ai_model
from ai_model import initialize_ai_model, get_ai_meal_plan, explain_recommendation

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


# ─── Pretty printing helpers ──────────────────────────────────────────────────

DIVIDER   = "─" * 60
BOLD_DIV  = "═" * 60


def section(title: str):
    print(f"\n{BOLD_DIV}")
    print(f"  {title}")
    print(BOLD_DIV)


def sub(title: str):
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)


# ─── Display functions ────────────────────────────────────────────────────────

def show_user_profile(profile: dict):
    section("USER PROFILE")
    for k, v in profile.items():
        print(f"  {k.capitalize():12s}  {v}")


def show_knowledge_base_sample():
    """Display a few foods from the knowledge base — mirrors Prolog listing/1."""
    from food_data import FOODS
    sub("Knowledge Base Sample (first 6 foods)")
    header = f"  {'Food':<18} {'Cal':>5} {'Prot':>5} {'Carbs':>6} {'Fat':>5}  Tags"
    print(header)
    print(f"  {'─'*18} {'─'*5} {'─'*5} {'─'*6} {'─'*5}  {'─'*25}")
    for name, f in list(FOODS.items())[:6]:
        tags = ", ".join(f["tags"][:3])
        print(f"  {name:<18} {f['calories']:>5} {f['protein']:>5} {f['carbs']:>6} {f['fat']:>5}  {tags}")


def show_rule_query(condition: str):
    """Show which foods pass the suitability predicate — mirrors Prolog query."""
    sub(f"Rule Query — suitable(Food, {condition})")
    rule = SUITABILITY_RULES.get(condition, SUITABILITY_RULES["general"])
    print(f"  Rule: {rule['description']}")
    print()
    for meal in ["breakfast", "lunch", "snack", "dinner"]:
        foods = get_suitable_foods(condition, meal)
        print(f"  {meal.capitalize():<12}: {', '.join(foods) if foods else '—'}")


def show_search_trace(trace: list, algorithm: str):
    sub(f"Search Trace — {algorithm}")
    for step in trace:
        if "event" in step:
            print(f"  [GOAL] Nodes explored: {step['nodes_explored']}  "
                  f"Final cost: {step['final_f_cost']}")
            continue
        if step.get("chosen") == "— none found —":
            print(f"  {step['meal'].upper():<12}  No suitable food found")
            continue
        meal  = step.get("meal", "").upper()
        chosen = step.get("chosen", "")
        cost   = step.get("cost", "")
        cands  = step.get("candidates", step.get("expanded", ""))
        print(f"  {meal:<12}  chosen: {chosen:<18}  cost: {str(cost):<8}  "
              f"candidates explored: {cands}")

        # Show top 3 alternatives for Greedy
        if "all_options" in step and len(step["all_options"]) > 1:
            others = [o for o in step["all_options"] if o["food"] != chosen][:2]
            for o in others:
                print(f"              alt:    {o['food']:<18}  cost: {o['cost']}")


def show_meal_plan(plan: dict, totals: dict, condition: str):
    section("RECOMMENDED MEAL PLAN")
    print(f"  Condition: {condition.replace('_', ' ').title()}\n")
    print(f"  {'Meal':<12}  {'Food':<20}  {'Cal':>5}  {'Prot':>5}  {'Carbs':>6}  {'Fat':>4}")
    print(f"  {'─'*12}  {'─'*20}  {'─'*5}  {'─'*5}  {'─'*6}  {'─'*4}")

    for meal, food_name in plan.items():
        if not food_name:
            print(f"  {meal.capitalize():<12}  {'—':20}")
            continue
        f = get_food_info(food_name)
        print(f"  {meal.capitalize():<12}  {food_name:<20}  "
              f"{f['calories']:>5}  {f['protein']:>5}  {f['carbs']:>6}  {f['fat']:>4}")

    print(f"\n  {'TOTAL':<34}  {totals['calories']:>5}  {totals['protein']:>5}  "
          f"{totals['carbs']:>6}  {totals['fat']:>4}")
    targets = get_targets(condition)
    print(f"  {'TARGET':<34}  {targets['calories']:>5}  {targets['protein']:>5}  "
          f"{targets['carbs']:>6}  {targets['fat']:>4}")


def show_violation_report(plan: dict, condition: str):
    sub("Prolog-Style Violation Report")
    any_violation = False
    for meal, food_name in plan.items():
        if not food_name:
            continue
        violations = check_violations(food_name, condition)
        status = "PASS"
        if violations:
            any_violation = True
            status = "FLAGGED"
        print(f"  {food_name:<20}  [{status}]"
              + (f"  -> {'; '.join(violations)}" if violations else ""))
    if not any_violation:
        print("\n  All foods passed rule validation.")


def show_comparison(condition: str):
    """Run both algorithms and compare their outputs."""
    section("ALGORITHM COMPARISON — Greedy BFS vs A*")

    print("\n  Running Greedy Best-First Search...")
    g_plan, g_totals, g_trace = greedy_search(condition)
    g_nodes = len(g_trace)

    print("  Running A* Search...")
    a_plan, a_totals, a_trace = astar_search(condition)
    a_nodes = next(
        (s["nodes_explored"] for s in a_trace if "nodes_explored" in s), len(a_trace)
    )

    targets = get_targets(condition)
    from heuristic import heuristic_cost
    g_cost = heuristic_cost(g_totals, targets)
    a_cost = heuristic_cost(a_totals, targets)

    print(f"\n  {'Metric':<28}  {'Greedy BFS':>12}  {'A*':>12}")
    print(f"  {'─'*28}  {'─'*12}  {'─'*12}")
    print(f"  {'Nodes explored':<28}  {g_nodes:>12}  {a_nodes:>12}")
    print(f"  {'Final heuristic cost':<28}  {g_cost:>12.1f}  {a_cost:>12.1f}")
    print(f"  {'Total calories':<28}  {g_totals['calories']:>12}  {a_totals['calories']:>12}")
    print(f"  {'Total protein (g)':<28}  {g_totals['protein']:>12}  {a_totals['protein']:>12}")
    print()
    for meal in ["breakfast", "lunch", "snack", "dinner"]:
        gf = g_plan.get(meal, "—")
        af = a_plan.get(meal, "—")
        match = "same" if gf == af else "different"
        print(f"  {meal.capitalize():<12}  Greedy: {str(gf):<18}  A*: {str(af):<18}  ({match})")


# ─── Matplotlib chart ─────────────────────────────────────────────────────────

def plot_nutrition_chart(totals: dict, condition: str, save_path: str = "nutrition_chart.png"):
    if not HAS_MATPLOTLIB:
        print("\n  [Chart skipped — matplotlib not installed. Run: pip install matplotlib]")
        return

    targets   = get_targets(condition)
    nutrients = ["calories", "protein", "carbs", "fat"]
    labels    = ["Calories (kcal)", "Protein (g)", "Carbs (g)", "Fat (g)"]
    actual    = [totals[n] for n in nutrients]
    target    = [targets[n] for n in nutrients]

    x    = range(len(nutrients))
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(
        f"Nutrition Advisor — {condition.replace('_', ' ').title()}",
        fontsize=14, fontweight="bold", y=1.01
    )

    # Left: grouped bar chart
    ax = axes[0]
    bars1 = ax.bar([i - 0.2 for i in x], actual, width=0.38,
                   label="Actual", color="#1D9E75", alpha=0.9)
    bars2 = ax.bar([i + 0.2 for i in x], target, width=0.38,
                   label="Target", color="#7F77DD", alpha=0.6)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=10, ha="right")
    ax.set_ylabel("Amount")
    ax.set_title("Actual vs Target")
    ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 3, str(int(bar.get_height())),
                ha="center", va="bottom", fontsize=9)

    # Right: % of target achieved
    ax2 = axes[1]
    pct = [round(a / t * 100, 1) if t > 0 else 0 for a, t in zip(actual, target)]
    colors = ["#1D9E75" if 80 <= p <= 120 else "#E24B4A" if p > 130 else "#EF9F27"
              for p in pct]
    bars = ax2.barh(labels, pct, color=colors, alpha=0.85)
    ax2.axvline(100, color="#7F77DD", linestyle="--", linewidth=1.2, label="Target (100%)")
    ax2.axvspan(80, 120, alpha=0.07, color="#1D9E75", label="Acceptable range")
    ax2.set_xlabel("% of daily target")
    ax2.set_title("Target Achievement")
    ax2.legend(fontsize=8)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    for bar, p in zip(bars, pct):
        ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                 f"{p}%", va="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"\n  Chart saved to: {save_path}")
    plt.close()  # Close without showing in terminal mode


# ─── Main entry point ─────────────────────────────────────────────────────────

def run_advisor(condition: str = "diabetic", algorithm: str = "greedy"):
    """
    Run the full nutrition advisor pipeline.

    Args:
        condition : one of diabetic | weight_loss | high_protein |
                    low_fat | vegetarian | general
        algorithm : greedy | astar | compare
    """
    profile = {
        "name":      "Student (CSA2001)",
        "condition": condition,
        "algorithm": algorithm,
        "goal":      {
            "diabetic":     "Manage blood sugar levels",
            "weight_loss":  "Reduce calorie intake",
            "high_protein": "Build muscle mass",
            "low_fat":      "Reduce fat intake",
            "vegetarian":   "Balanced vegetarian diet",
            "general":      "Maintain healthy nutrition",
        }.get(condition, "Healthy eating"),
    }

    show_user_profile(profile)
    show_knowledge_base_sample()
    show_rule_query(condition)

    if algorithm == "compare":
        show_comparison(condition)
        # Use greedy result for report
        plan, totals, trace = greedy_search(condition)
    elif algorithm == "astar":
        sub("Running A* Search")
        plan, totals, trace = astar_search(condition)
        show_search_trace(trace, "A* Search")
    else:
        sub("Running Greedy Best-First Search")
        plan, totals, trace = greedy_search(condition)
        show_search_trace(trace, "Greedy Best-First Search")

    show_meal_plan(plan, totals, condition)
    show_violation_report(plan, condition)
    plot_nutrition_chart(totals, condition)

    print(f"\n{BOLD_DIV}")
    print("  Run complete.")
    print(BOLD_DIV + "\n")


# ─── Interactive Terminal Menu ────────────────────────────────────────────────

def clear_screen():
    """Clear terminal screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def safe_input(prompt: str = "") -> str:
    """Safely get user input, handling EOF errors."""
    try:
        return input(prompt)
    except EOFError:
        return ""
    except KeyboardInterrupt:
        raise


def main_menu():
    """Display main menu and handle user input."""
    while True:
        clear_screen()
        section("DIET & NUTRITION ADVISOR - MAIN MENU")
        print("\n  1  Run Advisor (Interactive)")
        print("  2  View Food Database")
        print("  3  View All Rules")
        print("  4  Run Quick Demo (Diabetic + Greedy)")
        print("  5  Compare Algorithms (Greedy vs A*)")
        print("  6  [AI] AI-Powered Recommendations (ML Model)")
        print("  7  [AI] AI Analysis & Explanations")
        print("  8  Exit")
        print()
        
        choice = safe_input("  Enter your choice (1-8): ").strip()
        
        if choice == "1":
            run_interactive_advisor()
        elif choice == "2":
            show_food_database()
        elif choice == "3":
            show_all_rules()
        elif choice == "4":
            run_advisor("diabetic", "greedy")
            safe_input("\n  Press Enter to return to menu...")
        elif choice == "5":
            run_advisor("diabetic", "compare")
            safe_input("\n  Press Enter to return to menu...")
        elif choice == "6":
            clear_screen()
            show_ai_recommendations("diabetic")
            safe_input("\n  Press Enter to return to menu...")
        elif choice == "7":
            show_ai_explanation("diabetic")
        elif choice == "8":
            clear_screen()
            section("THANK YOU")
            print("  Goodbye!\n")
            break
        else:
            print("  [!] Invalid choice. Please try again.")
            safe_input("  Press Enter to continue...")


def run_interactive_advisor():
    """Interactive mode for selecting condition and algorithm."""
    clear_screen()
    section("INTERACTIVE ADVISOR SETUP")
    
    conditions = list(DAILY_TARGETS.keys())
    
    print("\n  Available Health Conditions:")
    print()
    for i, cond in enumerate(conditions, 1):
        desc = {
            "diabetic":     "Manage blood sugar levels",
            "weight_loss":  "Reduce calorie intake",
            "high_protein": "Build muscle mass",
            "low_fat":      "Reduce fat intake",
            "vegetarian":   "Balanced vegetarian diet",
            "general":      "Maintain healthy nutrition",
        }.get(cond, "Health optimization")
        print(f"  {i}  {cond.replace('_', ' ').title():<18} - {desc}")
    
    while True:
        try:
            cond_choice = int(safe_input("\n  Select condition (1-6): ").strip())
            if 1 <= cond_choice <= len(conditions):
                selected_condition = conditions[cond_choice - 1]
                break
            else:
                print("  [!] Invalid selection. Please enter 1-6.")
        except (ValueError, EOFError):
            print("  [!] Please enter a number.")
    
    algorithms = ["greedy", "astar", "compare"]
    print("\n  Available Algorithms:")
    print()
    print("  1  Greedy Best-First Search (faster)")
    print("  2  A* Search (optimal heuristic)")
    print("  3  Compare Both Algorithms")
    
    while True:
        try:
            algo_choice = int(safe_input("\n  Select algorithm (1-3): ").strip())
            if 1 <= algo_choice <= 3:
                selected_algorithm = algorithms[algo_choice - 1]
                break
            else:
                print("  [!] Invalid selection. Please enter 1-3.")
        except (ValueError, EOFError):
            print("  [!] Please enter a number.")
    
    print(f"\n  Running {selected_algorithm.upper()} for {selected_condition.replace('_', ' ').title()}...")
    print()
    run_advisor(selected_condition, selected_algorithm)
    safe_input("\n  Press Enter to return to menu...")


def show_food_database():
    """Display the complete food database."""
    clear_screen()
    section("FOOD DATABASE")
    from food_data import FOODS
    
    print(f"\n  Total foods in knowledge base: {len(FOODS)}\n")
    print(f"  {'Food':<20} {'Cal':>5} {'Prot':>5} {'Carbs':>6} {'Fat':>5}  Tags")
    print(f"  {'─'*20} {'─'*5} {'─'*5} {'─'*6} {'─'*5}  {'─'*30}")
    
    for name, f in FOODS.items():
        tags = ", ".join(f["tags"][:3])
        print(f"  {name:<20} {f['calories']:>5} {f['protein']:>5} {f['carbs']:>6} {f['fat']:>5}  {tags}")
    
    safe_input("\n  Press Enter to return to menu...")


def show_all_rules():
    """Display all suitability rules."""
    clear_screen()
    section("SUITABILITY RULES")
    
    print("\n  These rules define which foods are suitable for each health condition:\n")
    for condition, rule in SUITABILITY_RULES.items():
        print(f"  {condition.replace('_', ' ').upper():<18}")
        print(f"    → {rule['description']}")
        print()
    
    safe_input("  Press Enter to return to menu...")


# ─── AI-Powered Recommendations ────────────────────────────────────────────────

def show_ai_recommendations(condition: str):
    """Display AI-powered meal plan using self-learning model."""
    if not ai_model.ai_recommender or not ai_model.ai_recommender.is_trained:
        section("[AI] AI MEAL PLAN (SELF-LEARNING MODEL)")
        print("\n  Training AI model from food knowledge base...")
        initialize_ai_model()
    
    section("[AI] AI MEAL PLAN (SELF-LEARNING MODEL)")
    print(f"\n  Condition: {condition.replace('_', ' ').title()}")
    print(f"  Algorithm: Gradient Boosting Machine Learning Model")
    print(f"  Knowledge Base: 100 foods analyzed\n")
    
    ai_plan = get_ai_meal_plan(condition)
    
    print(f"\n  {'Meal':<12}  {'Food':<20}  {'Confidence':>10}  Top Alternatives")
    print(f"  {'─'*12}  {'─'*20}  {'─'*10}  {('─'*25)}")
    
    for meal in ["breakfast", "lunch", "snack", "dinner"]:
        if meal in ai_plan:
            recommendation = ai_plan[meal]
            food = recommendation["food"]
            confidence = recommendation["confidence"]
            alternatives = recommendation["alternatives"]
            
            if food:
                alt_str = ", ".join([f[0] for f, _ in alternatives[:2]]) if alternatives else "—"
                print(f"  {meal.capitalize():<12}  {food:<20}  {confidence*100:>9.1f}%  {alt_str}")
            else:
                print(f"  {meal.capitalize():<12}  {'—':<20}  {'—':>10}  —")
    
    # Calculate totals from AI recommendations
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
    for meal in ["breakfast", "lunch", "snack", "dinner"]:
        if meal in ai_plan and ai_plan[meal]["food"]:
            food_info = get_food_info(ai_plan[meal]["food"])
            for key in totals.keys():
                totals[key] += food_info[key]
    
    print(f"\n  {'TOTAL':<34}  {totals['calories']:>5}  {totals['protein']:>5}  "
          f"{totals['carbs']:>6}  {totals['fat']:>4}")
    targets = get_targets(condition)
    print(f"  {'TARGET':<34}  {targets['calories']:>5}  {targets['protein']:>5}  "
          f"{targets['carbs']:>6}  {targets['fat']:>4}")
    
    print("\n  " + DIVIDER)
    print("  [*] AI Model Insights:")
    print("  " + DIVIDER)
    
    # Show what the model learned
    feature_importance = ai_model.ai_recommender.get_feature_importance(condition)
    top_factors = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
    
    print("\n  Most Important Factors:")
    for i, (factor, importance) in enumerate(top_factors, 1):
        print(f"    {i}. {factor}: {importance*100:.1f}%")
    
    print()


def show_ai_explanation(condition: str):
    """Show detailed AI explanation for a food recommendation."""
    clear_screen()
    section("[AI] AI RECOMMENDATION ANALYSIS")
    
    if not ai_model.ai_recommender or not ai_model.ai_recommender.is_trained:
        initialize_ai_model()
    
    ai_plan = get_ai_meal_plan(condition)
    
    meals = ["breakfast", "lunch", "snack", "dinner"]
    print("\n  Select a meal to see AI analysis:\n")
    for i, meal in enumerate(meals, 1):
        if ai_plan[meal]["food"]:
            print(f"  {i}  {meal.capitalize()}: {ai_plan[meal]['food']}")
        else:
            print(f"  {i}  {meal.capitalize()}: No recommendation")
    
    print(f"  5  Back to menu")
    print()
    
    while True:
        try:
            choice = int(safe_input("  Select meal (1-5): ").strip())
            if 1 <= choice <= 4:
                meal = meals[choice - 1]
                if ai_plan[meal]["food"]:
                    explanation = explain_recommendation(ai_plan[meal]["food"], condition)
                    print(explanation)
                break
            elif choice == 5:
                break
            else:
                print("  [!] Invalid selection.")
        except (ValueError, EOFError):
            print("  [!] Please enter a number.")
    
    safe_input("\n  Press Enter to return to menu...")


def run_cli_mode():
    """Legacy CLI mode for command-line arguments."""
    condition = sys.argv[1] if len(sys.argv) > 1 else None
    algorithm = sys.argv[2] if len(sys.argv) > 2 else None
    
    valid_conditions = list(DAILY_TARGETS.keys())
    valid_algorithms = ["greedy", "astar", "compare"]
    
    if condition and algorithm:
        if condition not in valid_conditions:
            print(f"Unknown condition '{condition}'. Choose from: {valid_conditions}")
            sys.exit(1)
        if algorithm not in valid_algorithms:
            print(f"Unknown algorithm '{algorithm}'. Choose from: {valid_algorithms}")
            sys.exit(1)
        run_advisor(condition, algorithm)
    else:
        main_menu()


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Support both CLI and interactive modes
    # CLI mode: python main.py <condition> <algorithm>
    # Interactive mode: python main.py
    try:
        if len(sys.argv) > 1:
            run_cli_mode()
        else:
            clear_screen()
            main_menu()
    except KeyboardInterrupt:
        print("\n\n  Interrupted. Goodbye!\n")
        sys.exit(0)
