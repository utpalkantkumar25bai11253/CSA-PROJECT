"""
food_data.py
============
Food knowledge base — replaces Prolog food_facts.pl
Each food entry mirrors the Prolog fact:
  food(Name, Calories, Protein_g, Carbs_g, Fat_g, [Tags])
"""

FOODS = {
    "oats":          {"calories": 150, "protein": 5,  "carbs": 27, "fat": 3,  "tags": ["breakfast", "veg", "low_sugar"]},
    "banana":        {"calories":  89, "protein": 1,  "carbs": 23, "fat": 0,  "tags": ["fruit", "veg", "high_sugar", "snack"]},
    "brown_rice":    {"calories": 215, "protein": 5,  "carbs": 45, "fat": 2,  "tags": ["lunch", "dinner", "veg", "low_fat"]},
    "chicken":       {"calories": 165, "protein": 31, "carbs":  0, "fat": 4,  "tags": ["lunch", "dinner", "protein", "non_veg"]},
    "dal":           {"calories": 116, "protein": 9,  "carbs": 20, "fat": 0,  "tags": ["lunch", "dinner", "veg", "protein"]},
    "egg":           {"calories":  78, "protein": 6,  "carbs":  1, "fat": 5,  "tags": ["breakfast", "protein"]},
    "apple":         {"calories":  95, "protein": 0,  "carbs": 25, "fat": 0,  "tags": ["fruit", "snack", "low_sodium", "veg"]},
    "milk":          {"calories": 122, "protein": 8,  "carbs": 12, "fat": 5,  "tags": ["breakfast", "dairy"]},
    "roti":          {"calories": 120, "protein": 3,  "carbs": 25, "fat": 1,  "tags": ["lunch", "dinner", "veg"]},
    "paneer":        {"calories": 265, "protein": 18, "carbs":  4, "fat": 20, "tags": ["veg", "protein", "high_fat", "lunch"]},
    "spinach":       {"calories":  23, "protein": 3,  "carbs":  4, "fat": 0,  "tags": ["veg", "low_calorie", "iron", "lunch", "dinner"]},
    "sweet_potato":  {"calories": 103, "protein": 2,  "carbs": 24, "fat": 0,  "tags": ["lunch", "dinner", "veg", "low_fat"]},
    "lentil_soup":   {"calories": 140, "protein": 9,  "carbs": 24, "fat": 2,  "tags": ["lunch", "veg", "protein"]},
    "curd":          {"calories":  59, "protein": 3,  "carbs":  5, "fat": 3,  "tags": ["breakfast", "dairy", "probiotic", "snack"]},
    "almonds":       {"calories": 164, "protein": 6,  "carbs":  6, "fat": 14, "tags": ["snack", "protein", "healthy_fat"]},
    "moong_dal":     {"calories": 105, "protein": 7,  "carbs": 19, "fat": 0,  "tags": ["breakfast", "lunch", "veg", "protein", "low_fat"]},
    "grilled_fish":  {"calories": 140, "protein": 26, "carbs":  0, "fat": 3,  "tags": ["lunch", "dinner", "protein", "non_veg", "low_fat"]},
    "tomato":        {"calories":  18, "protein": 1,  "carbs":  4, "fat": 0,  "tags": ["veg", "low_calorie", "low_sodium", "snack"]},
    "peanut_butter": {"calories": 188, "protein": 8,  "carbs":  6, "fat": 16, "tags": ["breakfast", "snack", "protein", "healthy_fat"]},
    "oatmeal_bar":   {"calories": 190, "protein": 4,  "carbs": 30, "fat": 6,  "tags": ["snack", "breakfast"]},
    "boiled_potato": {"calories": 130, "protein": 3,  "carbs": 30, "fat": 0,  "tags": ["lunch", "dinner", "veg"]},
    "chicken_soup":  {"calories": 110, "protein": 12, "carbs":  8, "fat": 3,  "tags": ["dinner", "lunch", "protein", "non_veg", "low_fat"]},
    "rajma":         {"calories": 127, "protein": 9,  "carbs": 23, "fat": 0,  "tags": ["lunch", "dinner", "veg", "protein"]},
    "poha":          {"calories": 180, "protein": 4,  "carbs": 33, "fat": 4,  "tags": ["breakfast", "veg"]},
    "sprouts":       {"calories":  82, "protein": 6,  "carbs": 15, "fat": 0,  "tags": ["breakfast", "snack", "veg", "protein", "low_fat"]},
    
    # Additional fruits (26-35)
    "orange":        {"calories":  47, "protein": 1,  "carbs": 12, "fat": 0,  "tags": ["fruit", "snack", "vitamin_c"]},
    "strawberry":    {"calories":  32, "protein": 1,  "carbs":  8, "fat": 0,  "tags": ["fruit", "snack", "low_calorie"]},
    "mango":         {"calories":  60, "protein": 1,  "carbs": 15, "fat": 0,  "tags": ["fruit", "snack", "high_sugar"]},
    "grapes":        {"calories":  67, "protein": 1,  "carbs": 17, "fat": 0,  "tags": ["fruit", "snack", "high_sugar"]},
    "watermelon":    {"calories":  30, "protein": 1,  "carbs":  8, "fat": 0,  "tags": ["fruit", "snack", "low_calorie"]},
    "papaya":        {"calories":  43, "protein": 1,  "carbs": 11, "fat": 0,  "tags": ["fruit", "snack", "enzyme"]},
    "guava":         {"calories":  68, "protein": 3,  "carbs": 14, "fat": 1,  "tags": ["fruit", "snack", "protein"]},
    "pineapple":     {"calories":  50, "protein": 1,  "carbs": 13, "fat": 0,  "tags": ["fruit", "snack", "enzyme"]},
    "kiwi":          {"calories":  61, "protein": 1,  "carbs": 15, "fat": 0,  "tags": ["fruit", "snack", "vitamin_c"]},
    "pomegranate":   {"calories":  83, "protein": 2,  "carbs": 19, "fat": 1,  "tags": ["fruit", "snack", "antioxidant"]},
    
    # Additional vegetables (36-50)
    "broccoli":      {"calories":  34, "protein": 3,  "carbs":  7, "fat": 0,  "tags": ["veg", "low_calorie", "protein"]},
    "carrot":        {"calories":  41, "protein": 1,  "carbs": 10, "fat": 0,  "tags": ["veg", "snack", "vitamin_a"]},
    "cucumber":      {"calories":  16, "protein": 1,  "carbs":  4, "fat": 0,  "tags": ["veg", "low_calorie", "hydrating"]},
    "bell_pepper":   {"calories":  31, "protein": 1,  "carbs":  7, "fat": 0,  "tags": ["veg", "low_calorie", "vitamin_c"]},
    "cauliflower":   {"calories":  25, "protein": 2,  "carbs":  5, "fat": 0,  "tags": ["veg", "low_calorie"]},
    "cabbage":       {"calories":  22, "protein": 1,  "carbs":  5, "fat": 0,  "tags": ["veg", "low_calorie"]},
    "onion":         {"calories":  40, "protein": 1,  "carbs": 10, "fat": 0,  "tags": ["veg", "flavor"]},
    "garlic":        {"calories":  149, "protein": 6,  "carbs": 33, "fat": 1,  "tags": ["veg", "flavor"]},
    "green_beans":   {"calories":  31, "protein": 2,  "carbs":  7, "fat": 0,  "tags": ["veg", "low_calorie"]},
    "peas":          {"calories":  81, "protein": 5,  "carbs": 14, "fat": 0,  "tags": ["veg", "protein"]},
    "beetroot":      {"calories":  43, "protein": 2,  "carbs": 10, "fat": 0,  "tags": ["veg", "iron"]},
    "radish":        {"calories":  16, "protein": 1,  "carbs":  3, "fat": 0,  "tags": ["veg", "low_calorie"]},
    "mushroom":      {"calories":  22, "protein": 3,  "carbs":  3, "fat": 0,  "tags": ["veg", "low_calorie", "protein"]},
    "zucchini":      {"calories":  21, "protein": 1,  "carbs":  4, "fat": 0,  "tags": ["veg", "low_calorie"]},
    "pumpkin":       {"calories":  26, "protein": 1,  "carbs":  7, "fat": 0,  "tags": ["veg", "low_calorie"]},
    
    # Additional proteins (51-65)
    "fish":          {"calories": 100, "protein": 22, "carbs":  0, "fat": 1,  "tags": ["protein", "non_veg", "low_fat", "omega3"]},
    "mutton":        {"calories": 215, "protein": 23, "carbs":  0, "fat": 13, "tags": ["protein", "non_veg", "high_fat"]},
    "pork":          {"calories": 242, "protein": 27, "carbs":  0, "fat": 14, "tags": ["protein", "non_veg", "high_fat"]},
    "tofu":          {"calories":  76, "protein": 8,  "carbs":  2, "fat": 5,  "tags": ["protein", "veg", "low_fat"]},
    "chicken_breast": {"calories": 165, "protein": 31, "carbs":  0, "fat": 4,  "tags": ["protein", "non_veg", "low_fat"]},
    "turkey":        {"calories": 135, "protein": 30, "carbs":  0, "fat": 1,  "tags": ["protein", "non_veg", "low_fat"]},
    "black_beans":   {"calories": 132, "protein": 9,  "carbs": 24, "fat": 1,  "tags": ["protein", "veg", "plant_protein"]},
    "chickpeas":     {"calories": 164, "protein": 9,  "carbs": 27, "fat": 3,  "tags": ["protein", "veg", "plant_protein"]},
    "peas_protein":  {"calories":  81, "protein": 5,  "carbs": 14, "fat": 0,  "tags": ["protein", "veg", "plant_protein"]},
    "tempeh":        {"calories": 193, "protein": 19, "carbs": 10, "fat": 11, "tags": ["protein", "veg", "fermented"]},
    "seitan":        {"calories": 370, "protein": 25, "carbs": 14, "fat": 17, "tags": ["protein", "veg", "gluten"]},
    "lentils":       {"calories": 116, "protein": 9,  "carbs": 20, "fat": 0,  "tags": ["protein", "veg", "plant_protein"]},
    "chickpea_flour": {"calories": 387, "protein": 20, "carbs": 67, "fat": 6,  "tags": ["protein", "veg", "flour"]},
    "soy_chunks":    {"calories": 345, "protein": 52, "carbs": 33, "fat": 0,  "tags": ["protein", "veg", "textured"]},
    "cottage_cheese": {"calories":  98, "protein": 11, "carbs":  4, "fat": 5,  "tags": ["protein", "dairy"]},
    
    # Additional grains & carbs (66-75)
    "white_rice":    {"calories": 130, "protein": 3,  "carbs": 28, "fat": 0,  "tags": ["grain", "veg", "low_fat"]},
    "quinoa":        {"calories": 120, "protein": 4,  "carbs": 21, "fat": 2,  "tags": ["grain", "veg", "complete_protein"]},
    "barley":        {"calories": 354, "protein": 12, "carbs": 77, "fat": 2,  "tags": ["grain", "veg", "fiber"]},
    "pasta":         {"calories": 131, "protein": 5,  "carbs": 25, "fat": 1,  "tags": ["grain", "veg", "refined"]},
    "bread":         {"calories": 265, "protein": 9,  "carbs": 49, "fat": 3,  "tags": ["grain", "veg"]},
    "naan":          {"calories": 262, "protein": 8,  "carbs": 42, "fat": 7,  "tags": ["grain", "veg", "bread"]},
    "whole_wheat":   {"calories": 340, "protein": 14, "carbs": 72, "fat": 2,  "tags": ["grain", "veg", "high_fiber"]},
    "corn":          {"calories":  86, "protein": 3,  "carbs": 19, "fat": 1,  "tags": ["grain", "veg", "snack"]},
    "flattened_rice": {"calories": 350, "protein": 6,  "carbs": 80, "fat": 0,  "tags": ["grain", "veg", "breakfast"]},
    "millet":        {"calories": 378, "protein": 11, "carbs": 73, "fat": 4,  "tags": ["grain", "veg", "gluten_free"]},
    
    # Additional dairy & supplements (76-85)
    "greek_yogurt":  {"calories":  59, "protein": 10, "carbs":  3, "fat": 0,  "tags": ["dairy", "protein", "probiotic"]},
    "cheese":        {"calories": 402, "protein": 25, "carbs":  1, "fat": 33, "tags": ["dairy", "protein", "high_fat"]},
    "ghee":          {"calories": 892, "protein": 0,  "carbs":  0, "fat": 99, "tags": ["dairy", "fat", "cooking"]},
    "butter":        {"calories": 717, "protein": 1,  "carbs":  0, "fat": 81, "tags": ["dairy", "fat", "cooking"]},
    "buttermilk":    {"calories":  40, "protein": 4,  "carbs":  5, "fat": 0,  "tags": ["dairy", "fermented"]},
    "paneer_bhurji": {"calories": 180, "protein": 15, "carbs":  3, "fat": 12, "tags": ["dairy", "protein", "lunch"]},
    "kheer":         {"calories": 120, "protein": 4,  "carbs": 18, "fat": 4,  "tags": ["dairy", "dessert", "snack"]},
    "lassi":         {"calories":  80, "protein": 5,  "carbs": 12, "fat": 1,  "tags": ["dairy", "beverage"]},
    "whey_protein":  {"calories": 110, "protein": 25, "carbs":  3, "fat": 1,  "tags": ["protein", "supplement"]},
    "honey":         {"calories": 304, "protein": 0,  "carbs": 82, "fat": 0,  "tags": ["sweetener", "snack"]},
    
    # Additional nuts & seeds (86-95)
    "walnuts":       {"calories": 654, "protein": 15, "carbs": 14, "fat": 65, "tags": ["snack", "protein", "healthy_fat"]},
    "cashews":       {"calories": 553, "protein": 18, "carbs": 30, "fat": 44, "tags": ["snack", "protein", "healthy_fat"]},
    "peanuts":       {"calories": 567, "protein": 26, "carbs": 16, "fat": 49, "tags": ["snack", "protein", "healthy_fat"]},
    "sunflower_seeds": {"calories": 584, "protein": 20, "carbs": 20, "fat": 51, "tags": ["snack", "protein", "healthy_fat"]},
    "pumpkin_seeds": {"calories": 446, "protein": 19, "carbs": 16, "fat": 36, "tags": ["snack", "protein", "healthy_fat"]},
    "flaxseeds":     {"calories": 534, "protein": 18, "carbs": 29, "fat": 42, "tags": ["snack", "protein", "omega3"]},
    "chia_seeds":    {"calories": 486, "protein": 17, "carbs": 42, "fat": 31, "tags": ["snack", "protein", "omega3"]},
    "sesame_seeds":  {"calories": 563, "protein": 18, "carbs": 24, "fat": 50, "tags": ["snack", "protein", "calcium"]},
    "coconut":       {"calories": 354, "protein": 3,  "carbs": 15, "fat": 33, "tags": ["snack", "fat", "tropical"]},
    "dates":         {"calories": 282, "protein": 3,  "carbs": 75, "fat": 0,  "tags": ["snack", "sweetener", "energy"]},
    
    # Additional prepared dishes (96-100)
    "biryani":       {"calories": 280, "protein": 12, "carbs": 45, "fat": 5,  "tags": ["lunch", "dinner", "rice_dish"]},
    "masala_dosa":   {"calories": 300, "protein": 8,  "carbs": 50, "fat": 5,  "tags": ["breakfast", "lunch", "south_indian"]},
    "idli":          {"calories": 138, "protein": 5,  "carbs": 25, "fat": 1,  "tags": ["breakfast", "south_indian"]},
    "samosa":        {"calories": 262, "protein": 6,  "carbs": 30, "fat": 13, "tags": ["snack", "fried", "indian"]},
    "momos":         {"calories": 180, "protein": 8,  "carbs": 25, "fat": 5,  "tags": ["snack", "lunch", "asian"]},
}
