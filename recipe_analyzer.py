def analyze_recipes(recipe_list: str, call_llm) -> str:
    """
    Agent 3: Analyzes recipes in detail with nutrition and costs
    
    Args:
        recipe_list: List of recipes from Agent 2
        call_llm: Function to call the LLM
        
    Returns:
        Detailed recipe analysis with nutrition, costs, and scores (CONCISE VERSION)
    """
    
    print('recipe_list_agent_3',recipe_list)
    system_prompt = """You are a Recipe Analyzer agent for a recipe management system.

Your task is to:
1. Take each recipe from the search results
2. Provide CONCISE analysis for each recipe including:
   - Key ingredients (5-7 main items only, not full list)
   - Step-by-step cooking instructions (2-3 brief steps, one line each)
   - Nutritional information per serving (macros only)
   - Estimated total cost
   - Allergen check


IMPORTANT: 
- Provide 2-3 clear cooking steps (one line each)
- Keep each recipe analysis concise
- NO full ingredient lists with quantities
- Focus on KEY information only
- Total output should be concise and scannable

Output ONLY the analysis, nothing else."""

    return call_llm(system_prompt, recipe_list, agent_name='recipe_analyzer')