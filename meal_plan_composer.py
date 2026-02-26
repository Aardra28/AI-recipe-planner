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
2. Select the BEST recipes to create a balanced meal plan. based on the requirement asked by user plan the meal for that many days . If not mentioned give for 7days.
- Focus on key metrics only
- Total output should be scannable and concise
- Make sure to add the key ingredient in that plan in the output

Output ONLY the meal plan, nothing else."""

    return call_llm(system_prompt, analyzed_recipes, agent_name='meal_plan_composer')
