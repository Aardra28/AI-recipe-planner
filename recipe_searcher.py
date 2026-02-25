def search_recipes(preferences: str, call_llm) -> str:
    """
    Agent 2: Searches for recipes matching preferences
    
    Args:
        preferences: Structured preference summary from Agent 1
        call_llm: Function to call the LLM
        
    Returns:
        List of recipe titles with previews and sources
    """
    
    
    print('preferences_agent_2',preferences)
    system_prompt = """You are a Recipe Searcher agent for a recipe management system.

Your task is to:
1. Read the preference summary provided
2. Generate 8-12 diverse recipe candidates that match the preferences
3. Ensure variety across:
   - Different cuisines mentioned in preferences
   - Different protein sources (if applicable)
   - Different cooking methods (curry, grilled, baked, stir-fry, etc.)
   - Breakfast, lunch, and dinner options

4. For each recipe, provide:
   - Recipe name
   - Cuisine type
   - Main protein/ingredients
   - Brief description (2-3 sentences)
   - Estimated cooking time
   - Difficulty level (Easy/Medium/Hard)

5. Important filters:
   - EXCLUDE any recipes with allergens mentioned in restrictions
   - ONLY include proteins that are allowed
   - Stay within the cooking time limit
   - Match the cuisine preferences

Critical point : make sure to always stick to what the user asked and his preference.
Be creative, diverse, and ensure all recipes strictly match the user's preferences and restrictions.
Output ONLY the recipe list, nothing else."""

    return call_llm(system_prompt, preferences, agent_name='recipe_searcher')