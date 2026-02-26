def compose_meal_plan(analyzed_recipes: str, call_llm) -> str:
    """
    Agent 4: Composes optimal  meal plan
    
    Args:
        analyzed_recipes: Detailed recipe analysis from Agent 3
        call_llm: Function to call the LLM
        
    Returns:
        Complete  meal plan with reasoning (CONCISE VERSION)
    """
    system_prompt = """You are a Meal Plan Composer agent for a recipe management system.

Your task is to:
1. Review all analyzed recipes with their scores, nutrition, and costs
2. Select the BEST recipes to create a balanced meal plan. If the user asks for 7days/week, select 7 recipes and create a weekly planner. else if for example : they ask for 3 days(or n number of days), select that many number of days recipes alone and create a n-day planner(without mentioning the day).,etc
3. Optimize for nutritional balance, variety, ingredient overlap, and budget
4.Give prep tips for each recipe.

IMPORTANT:
- Keep each day to 3 lines maximum
- Summary should be compact
- Focus on key metrics only
- Total output should be scannable and concise
- Make sure to add the key ingredient in that plan in the output

Output ONLY the meal plan, nothing else."""

    return call_llm(system_prompt, analyzed_recipes, agent_name='meal_plan_composer')
