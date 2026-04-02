"""
ai_model.py
===========
Machine Learning model for intelligent dietary recommendations
Learns patterns from the food database to provide self-thinking suggestions
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from food_data import FOODS
from health_rules import SUITABILITY_RULES
from heuristic import DAILY_TARGETS

# ─── Data preparation ─────────────────────────────────────────────────────────

def prepare_training_data():
    """
    Prepare training data from food database for each health condition.
    
    Returns:
        dict: Training data for each condition with features and labels
    """
    training_data = {}
    
    for condition in list(DAILY_TARGETS.keys()):
        X = []  # Features
        y = []  # Labels (1 = suitable, 0 = unsuitable)
        
        rule_check = SUITABILITY_RULES[condition]["check"]
        
        for food_name, food_info in FOODS.items():
            # Extract features
            features = [
                food_info["calories"],
                food_info["protein"],
                food_info["carbs"],
                food_info["fat"],
                # Derived features
                food_info["protein"] / (food_info["calories"] + 1),  # protein ratio
                food_info["carbs"] / (food_info["calories"] + 1),    # carbs ratio
                food_info["fat"] / (food_info["calories"] + 1),      # fat ratio
                len(food_info["tags"]),  # number of tags
            ]
            
            X.append(features)
            
            # Determine label using the suitability rule
            is_suitable = 1 if rule_check(food_info) else 0
            y.append(is_suitable)
        
        training_data[condition] = {
            "X": np.array(X),
            "y": np.array(y),
            "food_names": list(FOODS.keys())
        }
    
    return training_data


# ─── Model training ───────────────────────────────────────────────────────────

class AIFoodRecommender:
    """Self-learning AI model for dietary recommendations."""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.training_data = prepare_training_data()
        self.is_trained = False
    
    def train(self):
        """Train models for each health condition."""
        print("\n  [AI] Training Machine Learning Models...\n")
        
        for condition, data in self.training_data.items():
            X = data["X"]
            y = data["y"]
            
            # Standardize features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Check if we have both classes
            unique_classes = len(set(y))
            
            if unique_classes < 2:
                # For conditions with all one class, create a simple probability model
                # based on feature similarity
                model = RandomForestClassifier(
                    n_estimators=50,
                    max_depth=3,
                    random_state=42,
                    class_weight='balanced'
                )
                # Artificially create some negative samples by slightly modifying data
                X_aug = np.vstack([X_scaled, X_scaled * 1.5])
                y_aug = np.hstack([y, np.zeros(len(y), dtype=int)])
                model.fit(X_aug, y_aug)
            else:
                # Train random forest for multi-class data
                model = RandomForestClassifier(
                    n_estimators=100,
                    max_depth=8,
                    random_state=42,
                    class_weight='balanced'
                )
                model.fit(X_scaled, y)
            
            self.models[condition] = model
            self.scalers[condition] = scaler
            
            # Print training accuracy
            train_accuracy = model.score(X_scaled, y)
            print(f"  [+] {condition.replace('_', ' ').title():<20} - Accuracy: {train_accuracy*100:.1f}%")
        
        self.is_trained = True
        print("\n  [+] AI Model training complete!\n")
    
    def predict_suitability(self, food_name: str, condition: str) -> float:
        """
        Predict suitability of a food for a condition using AI model.
        
        Args:
            food_name: Name of the food
            condition: Health condition
        
        Returns:
            float: Probability that food is suitable (0-1)
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        if food_name not in FOODS or condition not in self.models:
            return 0.0
        
        food_info = FOODS[food_name]
        
        # Extract features
        features = np.array([[
            food_info["calories"],
            food_info["protein"],
            food_info["carbs"],
            food_info["fat"],
            food_info["protein"] / (food_info["calories"] + 1),
            food_info["carbs"] / (food_info["calories"] + 1),
            food_info["fat"] / (food_info["calories"] + 1),
            len(food_info["tags"]),
        ]])
        
        # Scale features
        X_scaled = self.scalers[condition].transform(features)
        
        # Get probability
        probability = self.models[condition].predict_proba(X_scaled)[0][1]
        
        return probability
    
    def get_ai_recommendations(self, condition: str, meal_type: str) -> list:
        """
        Get AI-powered recommendations for a meal using self-learning model.
        
        Args:
            condition: Health condition
            meal_type: Type of meal (breakfast, lunch, snack, dinner)
        
        Returns:
            list: Sorted list of (food_name, probability) tuples
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        # Filter foods for the meal type
        meal_foods = [
            (name, info) for name, info in FOODS.items()
            if meal_type in info.get("tags", [])
        ]
        
        # Get AI predictions
        predictions = []
        for food_name, food_info in meal_foods:
            prob = self.predict_suitability(food_name, condition)
            predictions.append((food_name, prob))
        
        # Sort by probability (highest first)
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        return predictions
    
    def get_feature_importance(self, condition: str) -> dict:
        """
        Get feature importance for a condition - shows what the model learned.
        
        Args:
            condition: Health condition
        
        Returns:
            dict: Feature names and their importance scores
        """
        if condition not in self.models:
            return {}
        
        model = self.models[condition]
        feature_names = [
            "Calories",
            "Protein (g)",
            "Carbs (g)",
            "Fat (g)",
            "Protein Ratio",
            "Carbs Ratio",
            "Fat Ratio",
            "Num Tags"
        ]
        
        importances = model.feature_importances_
        
        feature_importance = {
            name: importance
            for name, importance in zip(feature_names, importances)
        }
        
        return feature_importance


# Global AI model instance
ai_recommender = None


def initialize_ai_model():
    """Initialize and train the AI model."""
    global ai_recommender
    ai_recommender = AIFoodRecommender()
    ai_recommender.train()


def get_ai_meal_plan(condition: str) -> dict:
    """
    Generate a meal plan using AI-powered recommendations.
    
    Args:
        condition: Health condition
    
    Returns:
        dict: AI-recommended meal plan
    """
    global ai_recommender
    
    if not ai_recommender or not ai_recommender.is_trained:
        raise ValueError("AI model not initialized. Call initialize_ai_model() first.")
    
    meal_plan = {}
    meals = ["breakfast", "lunch", "snack", "dinner"]
    
    for meal in meals:
        recommendations = ai_recommender.get_ai_recommendations(condition, meal)
        
        if recommendations:
            # Get the top recommendation
            best_food, confidence = recommendations[0]
            meal_plan[meal] = {
                "food": best_food,
                "confidence": confidence,
                "alternatives": recommendations[1:4]  # Top 3 alternatives
            }
        else:
            meal_plan[meal] = {
                "food": None,
                "confidence": 0.0,
                "alternatives": []
            }
    
    return meal_plan


def explain_recommendation(food_name: str, condition: str) -> str:
    """
    Generate an explanation for why a food was recommended.
    
    Args:
        food_name: Name of the food
        condition: Health condition
    
    Returns:
        str: Explanation of the recommendation
    """
    global ai_recommender
    
    if not ai_recommender or not ai_recommender.is_trained:
        return "AI model not initialized."
    
    food = FOODS.get(food_name)
    if not food:
        return f"Food '{food_name}' not found in database."
    
    confidence = ai_recommender.predict_suitability(food_name, condition)
    feature_importance = ai_recommender.get_feature_importance(condition)
    
    # Find most important features
    top_features = sorted(
        feature_importance.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]
    
    explanation = f"\n  {food_name.upper()} for {condition.replace('_', ' ').upper()}\n"
    explanation += f"  Suitability Score: {confidence*100:.1f}%\n"
    explanation += f"\n  Nutritional Profile:\n"
    explanation += f"    • Calories: {food['calories']} kcal\n"
    explanation += f"    • Protein: {food['protein']}g\n"
    explanation += f"    • Carbs: {food['carbs']}g\n"
    explanation += f"    • Fat: {food['fat']}g\n"
    explanation += f"\n  AI Model Analysis:\n"
    explanation += f"    • Top Important Features:\n"
    for feature, importance in top_features:
        explanation += f"      - {feature}: {importance*100:.1f}%\n"
    
    if confidence > 0.7:
        explanation += f"\n  [YES] Strongly recommended by AI\n"
    elif confidence > 0.5:
        explanation += f"\n  [YES] Moderately recommended by AI\n"
    else:
        explanation += f"\n  [!] Weakly recommended by AI\n"
    
    return explanation
