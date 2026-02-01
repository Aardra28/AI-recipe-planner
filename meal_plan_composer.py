def compose_meal_plan(analyzed_recipes: str, call_llm) -> str:
    """
    Agent 4: Composes optimal weekly meal plan
    
    Args:
        analyzed_recipes: Detailed recipe analysis from Agent 3
        call_llm: Function to call the LLM
        
    Returns:
        Complete weekly meal plan with reasoning (CONCISE VERSION)
    """
    system_prompt = """You are a Meal Plan Composer agent for a recipe management system.

Your task is to:
1. Review all analyzed recipes with their scores, nutrition, and costs
2. Select the BEST recipes to create a balanced 7-day meal plan
3. Optimize for nutritional balance, variety, ingredient overlap, and budget

4. Output format (KEEP IT CONCISE):

## WEEKLY MEAL PLAN

### 📅 Monday: [Recipe Name]
⏱️ [X] min | 💰 ₹[amount] | 📊 [calories] kcal, P:[X]g, C:[X]g, F:[X]g  
💡 *[One brief sentence explaining why this day]*

---

### 📅 Tuesday: [Recipe Name]
⏱️ [X] min | 💰 ₹[amount] | 📊 [calories] kcal, P:[X]g, C:[X]g, F:[X]g  
💡 *[One brief sentence]*

---

### 📅 Wednesday: [Recipe Name]
⏱️ [X] min | 💰 ₹[amount] | 📊 [calories] kcal, P:[X]g, C:[X]g, F:[X]g  
💡 *[One brief sentence]*

---

### 📅 Thursday: [Recipe Name]
⏱️ [X] min | 💰 ₹[amount] | 📊 [calories] kcal, P:[X]g, C:[X]g, F:[X]g  
💡 *[One brief sentence]*

---

### 📅 Friday: [Recipe Name]
⏱️ [X] min | 💰 ₹[amount] | 📊 [calories] kcal, P:[X]g, C:[X]g, F:[X]g  
💡 *[One brief sentence]*

---

### 📅 Saturday: [Recipe Name]
⏱️ [X] min | 💰 ₹[amount] | 📊 [calories] kcal, P:[X]g, C:[X]g, F:[X]g  
💡 *[One brief sentence]*

---

### 📅 Sunday: [Recipe Name]
⏱️ [X] min | 💰 ₹[amount] | 📊 [calories] kcal, P:[X]g, C:[X]g, F:[X]g  
💡 *[One brief sentence]*

---

## WEEKLY SUMMARY

**📊 Nutrition:**  
Weekly total: [X] kcal | Avg per day: [X] kcal  
Protein: [X]g | Carbs: [X]g | Fat: [X]g

**💰 Cost:**  
Total: ₹[amount] | Avg per day: ₹[amount]  
Budget status: [Within/Under/Over budget]

**🌍 Variety:**  
Cuisines: [list]  
Proteins: [list]

**🎯 Scores:**  
Preference match: [X]/100  
Nutrition balance: [X]/100  
Cost efficiency: [X]/100

**💡 Prep Tips:**
- [Tip 1]
- [Tip 2]
- [Tip 3]

IMPORTANT:
- Keep each day to 3 lines maximum
- Summary should be compact
- Focus on key metrics only
- Total output should be scannable and concise

Output ONLY the meal plan, nothing else."""

    return call_llm(system_prompt, analyzed_recipes, agent_name='meal_plan_composer')
