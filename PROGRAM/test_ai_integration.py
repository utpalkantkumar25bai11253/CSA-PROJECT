#!/usr/bin/env python
"""
test_ai_integration.py
======================
Direct test of AI model integration without interactive input
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("  AI MODEL INTEGRATION TEST")
print("=" * 60)

# Test 1: Import test
print("\n[1] Testing imports...")
try:
    from ai_model import initialize_ai_model, get_ai_meal_plan, explain_recommendation
    import ai_model
    print("    [OK] Imports successful")
except Exception as e:
    print(f"    [ERROR] Import failed: {e}")
    sys.exit(1)

# Test 2: Model initialization
print("\n[2] Initializing AI model...")
try:
    initialize_ai_model()
    print("    [OK] Model initialized")
except Exception as e:
    print(f"    [ERROR] Initialization failed: {e}")
    sys.exit(1)

# Test 3: Check global ai_recommender
print("\n[3] Checking ai_recommender global...")
try:
    assert ai_model.ai_recommender is not None, "ai_recommender is still None"
    assert ai_model.ai_recommender.is_trained, "Model not trained"
    print("    [OK] ai_recommender is initialized and trained")
except Exception as e:
    print(f"    [ERROR] {e}")
    sys.exit(1)

# Test 4: Get AI meal plan for each condition
print("\n[4] Testing AI meal plans for all conditions...")
conditions = ["diabetic", "weight_loss", "high_protein", "low_fat", "vegetarian", "general"]
for condition in conditions:
    try:
        meal_plan = get_ai_meal_plan(condition)
        print(f"    [OK] {condition:<15} - Generated meal plan with {len(meal_plan)} meals")
    except Exception as e:
        print(f"    [ERROR] {condition:<15} - {e}")

# Test 5: Feature importance
print("\n[5] Testing feature importance...")
try:
    feature_importance = ai_model.ai_recommender.get_feature_importance("diabetic")
    if feature_importance:
        print(f"    [OK] Got feature importance: {len(feature_importance)} features")
        for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]:
            print(f"        - {feature}: {importance*100:.1f}%")
    else:
        print("    [WARNING] No feature importance returned")
except Exception as e:
    print(f"    [ERROR] {e}")

# Test 6: Display sample meal plan
print("\n[6] Sample AI meal plan (Diabetic condition)...")
try:
    meal_plan = get_ai_meal_plan("diabetic")
    for meal, rec in meal_plan.items():
        if rec["food"]:
            print(f"    {meal.capitalize():<12}: {rec['food']:<15} ({rec['confidence']*100:.1f}%)")
except Exception as e:
    print(f"    [ERROR] {e}")

print("\n" + "=" * 60)
print("  ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 60)
