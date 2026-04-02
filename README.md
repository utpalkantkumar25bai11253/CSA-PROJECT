# Diet & Nutrition Advisor

A terminal-based AI nutrition planning system that uses search algorithms (Greedy Best-First Search and A*) to recommend personalized meal plans based on health conditions.

## 🎯 Project Overview

**Course:** CSA2001 — Fundamentals in AI and ML (Project 3)

**Techniques Used:**
- Rule-based Knowledge Representation (Prolog-style rules in Python)
- Greedy Best-First Search Algorithm
- A* Search Algorithm
- Heuristic Cost Functions

## 📋 Features

- **Interactive Terminal Menu**: User-friendly interface to navigate all features
- **Multiple Health Conditions**: 
  - Diabetic (low carb)
  - Weight Loss (low calorie)
  - High Protein (muscle building)
  - Low Fat (fat reduction)
  - Vegetarian (plant-based)
  - General (balanced nutrition)
- **Multiple Algorithms**:
  - Greedy Best-First Search (faster)
  - A* Search (optimal heuristic)
  - Side-by-side algorithm comparison
- **Comprehensive Output**:
  - Recommended meal plans
  - Nutrition analysis with charts
  - Suitability rules and violations
  - Search traces (nodes explored, costs)

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Running the Application

**Interactive Mode (Recommended):**
```bash
python main.py
```

This launches an interactive menu where you can:
1. Run the advisor interactively (select condition and algorithm)
2. View the complete food database
3. View all health rules
4. Run a quick demo
5. Compare algorithms
6. Exit

**Command-Line Mode:**
```bash
python main.py <condition> <algorithm>
```

Examples:
```bash
python main.py diabetic greedy
python main.py weight_loss astar
python main.py general compare
```

## 📊 Menu Options

### 1. Run Advisor (Interactive)
- Select a health condition from 6 available options
- Choose an algorithm (Greedy, A*, or Compare)
- View personalized meal plan with:
  - Recommended foods for each meal
  - Nutritional totals vs. daily targets
  - Violation report
  - Visualization chart (if matplotlib installed)

### 2. View Food Database
- Browse all foods in the knowledge base
- See calories, protein, carbs, and fat for each food
- Check food tags (veg, non-veg, high_sugar, etc.)

### 3. View All Rules
- Display suitability criteria for each health condition
- Understand what makes a food suitable

### 4. Run Quick Demo
- Pre-configured demo: Diabetic condition + Greedy algorithm
- Good for testing the system quickly

### 5. Compare Algorithms
- Side-by-side comparison of Greedy vs A*
- View metrics like:
  - Nodes explored
  - Final heuristic cost
  - Total calories and nutrients
  - Meal recommendations

### 6. Exit
- Gracefully exit the application

## 📁 Project Structure

```
.
├── main.py                    # Main application with interactive menu
├── food_data.py              # Food knowledge base
├── health_rules.py           # Suitability rules and violation checks
├── heuristic.py              # Heuristic functions and daily targets
├── search.py                 # Greedy BFS and A* algorithms
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

### File Descriptions

- **main.py**: Core application with interactive terminal interface and display functions
- **food_data.py**: Knowledge base containing food items with nutritional information
- **health_rules.py**: Rule engine for checking food suitability by condition
- **heuristic.py**: Daily nutritional targets and heuristic cost calculations
- **search.py**: Implementation of Greedy Best-First Search and A* algorithms

## 🔍 Example Usage

### Interactive Session

```
════════════════════════════════════════════════════════════════
  DIET & NUTRITION ADVISOR - MAIN MENU
════════════════════════════════════════════════════════════════

  1  Run Advisor (Interactive)
  2  View Food Database
  3  View All Rules
  4  Run Quick Demo (Diabetic + Greedy)
  5  Compare Algorithms (Greedy vs A*)
  6  Exit

  Enter your choice (1-6): 1
```

Then select your health condition and algorithm for a personalized meal plan.

## 📈 Algorithm Comparison

The system can compare Greedy and A* algorithms on the same problem:

| Metric | Greedy BFS | A* Search |
|--------|-----------|-----------|
| Speed | Faster | Slightly slower |
| Optimality | Good heuristic | Optimal within heuristic |
| Nodes Explored | Fewer | May explore more |
| Final Cost | Near-optimal | Optimal |

## 📊 Output Features

1. **Meal Plan**:
   - Breakfast, Lunch, Snack, Dinner recommendations
   - Nutritional breakdown per meal
   - Total vs. daily targets

2. **Search Trace**:
   - Shows decision-making process
   - Lists candidate foods considered
   - Displays costs and alternatives

3. **Violation Report**:
   - Flags foods that don't meet criteria
   - Lists specific violations
   - Ensures rule compliance

4. **Visualization** (if matplotlib installed):
   - Grouped bar chart: Actual vs Target
   - Percentage achievement chart
   - Saved as `nutrition_chart.png`

## 🛠️ Customization

### Adding New Foods

Edit `food_data.py` and add to the `FOODS` dictionary:

```python
"Apple": {
    "calories": 95,
    "protein": 0,
    "carbs": 25,
    "fat": 0,
    "tags": ["veg", "fruit"]
},
```

### Adding New Health Conditions

1. Add to `DAILY_TARGETS` in `heuristic.py`
2. Add rule to `SUITABILITY_RULES` in `health_rules.py`
3. Add goal description in `main.py`

### Adjusting Daily Targets

Edit the `DAILY_TARGETS` dictionary in `heuristic.py`:

```python
DAILY_TARGETS = {
    "your_condition": {
        "calories": 2000,
        "protein": 50,
        "carbs": 250,
        "fat": 65,
    }
}
```

## 📚 Learning Outcomes

This project demonstrates:

- ✅ **CO2**: Informed search strategies (Greedy + A*)
- ✅ **CO4**: Problem analysis and AI system design
- ✅ **CO5**: Real-world AI application (nutrition planning)
- ✅ **CO6**: Rule-based logic (Prolog-style predicates in Python)

## 🐛 Troubleshooting

**Issue**: No nutrition chart displayed
- **Solution**: Install matplotlib: `pip install matplotlib`

**Issue**: Unicode characters not displaying properly
- **Solution**: Already handled via `sys.stdout.reconfigure(encoding='utf-8')`

**Issue**: Command not found
- **Solution**: Ensure Python is in PATH and all dependencies are installed

## 📝 Notes

- The system maintains rule consistency using a Prolog-like approach
- Heuristic functions guide search toward optimal nutrition goals
- All meal plans are validated against suitability rules
- The interactive interface is user-friendly and self-explanatory

## 🎓 Author

CSA2001 Student Project

## 📄 License

Educational - For CSA2001 course use only

---

**Enjoy your personalized meal planning with AI!** 🍽️🤖
