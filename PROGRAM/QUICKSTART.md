# Quick Start Guide - Terminal-Based Nutrition Advisor

## 🚀 Getting Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application

**For Interactive Menu (Recommended):**
```bash
python main.py
```

**For Direct Analysis:**
```bash
python main.py <condition> <algorithm>
```

### 3. Navigate & Explore
Use the interactive menu to explore different health conditions and algorithms.

---

## 📋 Available Conditions

| Condition | Purpose | Example Rule |
|-----------|---------|--------------|
| `diabetic` | Manage blood sugar | Low carbohydrates (< 15g) |
| `weight_loss` | Reduce calorie intake | Low calories (< 150 kcal) |
| `high_protein` | Build muscle | High protein (> 8g) |
| `low_fat` | Reduce fat intake | Low fat (< 5g) |
| `vegetarian` | Plant-based diet | Vegetarian foods only |
| `general` | Balanced nutrition | No restrictions |

---

## 🎯 Available Algorithms

| Algorithm | Speed | Use Case |
|-----------|-------|----------|
| `greedy` | Fast ⚡ | Quick recommendations |
| `astar` | Balanced ⚙️ | Optimal heuristic results |
| `compare` | Slower 🔄 | See both algorithms side-by-side |

---

## 💡 Command Examples

### Interactive Mode
```bash
python main.py
# Then select from menu:
# 1 - Run Advisor (Interactive)
# 2 - View Food Database
# 3 - View All Rules
# 4 - Run Quick Demo
# 5 - Compare Algorithms
# 6 - Exit
```

### Quick Demos
```bash
# Diabetic meal plan using Greedy search
python main.py diabetic greedy

# Weight loss plan using A* search
python main.py weight_loss astar

# Compare algorithms for vegetarian diet
python main.py vegetarian compare
```

---

## 📊 Output Includes

✅ **Recommended Meal Plan**
- Breakfast, Lunch, Snack, Dinner suggestions
- Nutritional breakdown per meal

✅ **Nutrition Analysis** 
- Total nutrients vs. daily targets
- Percentage achievement chart

✅ **Violation Report**
- Confirms all foods meet health criteria
- Flags any violations

✅ **Search Trace**
- Shows decision-making process
- Displays candidate foods considered

✅ **Visualization**
- Saves chart as `nutrition_chart.png`
- Grouped bar chart comparing actual vs target

---

## 🎮 Interactive Menu Features

### Option 1: Run Advisor (Interactive)
- Choose your health condition (6 options)
- Select algorithm (Greedy, A*, or Compare)
- Get personalized meal plan with full analysis

### Option 2: View Food Database
- Browse all 30+ foods in the knowledge base
- See complete nutritional information
- Check food tags and categories

### Option 3: View All Rules
- Display suitability criteria for each condition
- Understand what makes foods suitable

### Option 4: Run Quick Demo
- Pre-configured: Diabetic + Greedy
- Good for first-time testing

### Option 5: Compare Algorithms
- Side-by-side comparison: Greedy vs A*
- See which algorithm performs better
- Compare recommended meals and costs

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| No menu appears | Run with `python main.py` (no arguments) |
| "Unknown condition" error | Check condition spelling: diabetic, weight_loss, etc. |
| Missing nutrition chart | Install matplotlib: `pip install matplotlib` |
| Unicode characters garbled | Python will auto-configure UTF-8 (Windows) |

---

## 📁 File Overview

- **main.py** - Interactive terminal interface (START HERE)
- **food_data.py** - Food knowledge base (30+ foods)
- **health_rules.py** - Suitability predicates
- **heuristic.py** - Nutritional targets & cost functions
- **search.py** - Greedy & A* algorithms

---

## ⚡ Performance Notes

- **Greedy Search**: ~100ms (very fast)
- **A* Search**: ~150ms (still very fast)
- **Chart Generation**: ~500ms (if matplotlib installed)

---

## 🎓 Educational Focus

- **Search Algorithms**: See how Greedy and A* make decisions
- **Knowledge Representation**: Rule-based diet rules
- **Heuristics**: How distance to targets guides search
- **AI Optimization**: Finding best meal combinations

---

## 💬 Example Session

```
════════════════════════════════════════════════════════════
  DIET & NUTRITION ADVISOR - MAIN MENU
════════════════════════════════════════════════════════════

  1  Run Advisor (Interactive)
  2  View Food Database
  3  View All Rules
  4  Run Quick Demo (Diabetic + Greedy)
  5  Compare Algorithms (Greedy vs A*)
  6  Exit

  Enter your choice (1-6): 1

Available Health Conditions:

  1  Diabetic - Manage blood sugar levels
  2  Weight Loss - Reduce calorie intake
  ...
  
  Select condition (1-6): 1
  
Available Algorithms:

  1  Greedy Best-First Search (faster)
  2  A* Search (optimal heuristic)
  3  Compare Both Algorithms
  
  Select algorithm (1-3): 1
  
Running greedy for diabetic...

════════════════════════════════════════════════════════════
  RECOMMENDED MEAL PLAN
════════════════════════════════════════════════════════════

  Meal          Food               Cal    Prot    Carbs    Fat
  ──────────    ──────────────     ────   ────    ─────    ───
  Breakfast     egg                78      6        1       5
  Lunch         paneer             265    18        4      20
  Snack         almonds            170    6         6      15
  Dinner        chicken            165    31        0       4

  TOTAL                            678    61       11      44
  TARGET                          1500    85      120      50

  Press Enter to return to menu...
```

---

**Enjoy your AI-powered nutrition planning! 🍽️🤖**
