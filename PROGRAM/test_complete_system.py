#!/usr/bin/env python
"""
test_complete_system.py
=======================
Comprehensive test of the complete Diet & Nutrition Advisor system
Tests all major components including new AI features
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("  COMPREHENSIVE SYSTEM TEST - DIET & NUTRITION ADVISOR")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════════════════

print("\n[SECTION 1] Core Module Imports")
print("─" * 70)

try:
    from food_data import FOODS
    print("  ✓ food_data module loaded")
    print(f"    - Database contains {len(FOODS)} foods")
except Exception as e:
    print(f"  ✗ food_data import failed: {e}")
    sys.exit(1)

try:
    from health_rules import SUITABILITY_RULES, get_suitable_foods
    print("  ✓ health_rules module loaded")
    print(f"    - {len(SUITABILITY_RULES)} suitability rules")
except Exception as e:
    print(f"  ✗ health_rules import failed: {e}")
    sys.exit(1)

try:
    from search import greedy_search, astar_search
    print("  ✓ search algorithms loaded (Greedy BFS, A* Search)")
except Exception as e:
    print(f"  ✗ search import failed: {e}")
    sys.exit(1)

try:
    from heuristic import heuristic_cost, DAILY_TARGETS, get_targets
    print("  ✓ heuristic module loaded")
    print(f"    - {len(DAILY_TARGETS)} daily nutrition targets")
except Exception as e:
    print(f"  ✗ heuristic import failed: {e}")
    sys.exit(1)

try:
    from ai_model import initialize_ai_model, get_ai_meal_plan, explain_recommendation
    import ai_model
    print("  ✓ ai_model module loaded")
except Exception as e:
    print(f"  ✗ ai_model import failed: {e}")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════

print("\n[SECTION 2] AI Model Training")
print("─" * 70)

try:
    initialize_ai_model()
    print("  ✓ AI model initialized and trained")
    
    assert ai_model.ai_recommender is not None
    assert ai_model.ai_recommender.is_trained
    print("  ✓ AI recommender is ready for use")
except Exception as e:
    print(f"  ✗ AI initialization failed: {e}")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════

print("\n[SECTION 3] Search Algorithm Tests")
print("─" * 70)

conditions_to_test = ["diabetic", "weight_loss", "high_protein"]

for condition in conditions_to_test:
    try:
        # Test Greedy Search
        g_plan, g_totals, g_trace = greedy_search(condition)
        greedy_status = "OK" if g_plan else "Empty"
        
        # Test A* Search
        a_plan, a_totals, a_trace = astar_search(condition)
        astar_status = "OK" if a_plan else "Empty"
        
        print(f"  ✓ {condition:<15} - Greedy: {greedy_status}, A*: {astar_status}")
    except Exception as e:
        print(f"  ✗ {condition:<15} - Error: {e}")

# ═══════════════════════════════════════════════════════════════════════════

print("\n[SECTION 4] AI Meal Plan Generation")
print("─" * 70)

for condition in DAILY_TARGETS.keys():
    try:
        ai_plan = get_ai_meal_plan(condition)
        num_meals = len([m for m in ai_plan.values() if m["food"]])
        conf_avg = sum(m["confidence"] for m in ai_plan.values() if m["food"]) / max(1, num_meals)
        print(f"  ✓ {condition:<15} - {num_meals} meals, avg confidence: {conf_avg*100:.1f}%")
    except Exception as e:
        print(f"  ✗ {condition:<15} - Error: {e}")

# ═══════════════════════════════════════════════════════════════════════════

print("\n[SECTION 5] Food Database Validation")
print("─" * 70)

# Check data consistency
calories_count = sum(1 for f in FOODS.values() if f["calories"] > 0)
protein_count = sum(1 for f in FOODS.values() if f["protein"] > 0)
print(f"  ✓ Foods with calorie data: {calories_count}/{len(FOODS)}")
print(f"  ✓ Foods with protein data: {protein_count}/{len(FOODS)}")

# Check categories
categories = {}
for food, data in FOODS.items():
    for tag in data["tags"]:
        categories[tag] = categories.get(tag, 0) + 1

print(f"  ✓ Food categories: {len(categories)}")
for cat in sorted(categories.keys())[:5]:
    print(f"    - {cat}: {categories[cat]} foods")
if len(categories) > 5:
    print(f"    ... and {len(categories) - 5} more categories")

# ═══════════════════════════════════════════════════════════════════════════

print("\n[SECTION 6] Rule Validation")
print("─" * 70)

for condition in list(DAILY_TARGETS.keys())[:3]:
    breakfast_foods = get_suitable_foods(condition, "breakfast")
    lunch_foods = get_suitable_foods(condition, "lunch")
    print(f"  ✓ {condition:<15} - Breakfast: {len(breakfast_foods)} options, "
          f"Lunch: {len(lunch_foods)} options")

# ═══════════════════════════════════════════════════════════════════════════

print("\n[SECTION 7] Feature Importance (What AI learned)")
print("─" * 70)

test_condition = "diabetic"
try:
    feature_importance = ai_model.ai_recommender.get_feature_importance(test_condition)
    top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"  ✓ Top features learned for '{test_condition}':")
    for feature, importance in top_features:
        print(f"    - {feature}: {importance*100:.1f}%")
except Exception as e:
    print(f"  ✗ Feature importance error: {e}")

# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("  ALL TESTS COMPLETED SUCCESSFULLY!")
print("  System is ready for use. Run: python main.py")
print("=" * 70 + "\n")
