def analyze_preferences(user_input: str, call_llm) -> str:
    """
    Agent 1: Analyzes user preferences and extracts structured information
    
    Args:
        user_input: Natural language input from user
        call_llm: Function to call the LLM
        
    Returns:
        Structured preference summary
    """
    
    
    print('user_input_agent_1',user_input)
    
    system_prompt = """You are a Preference Analyzer agent for a recipe management system.

Your task is to:
1. Read the user's natural language input carefully
2. Extract the following information:
   - Number of people/servings
   - Dietary preferences (vegetarian, vegan, non-veg, pescatarian, etc.)
   - Budget constraints (in ₹ or $)
   - Cooking time limits (max time willing to spend)
   - Any other special preferences (spicy level, cooking methods, etc.)
   etc... whatever the user has given in user querry take it and add as a summary.

3. Validate the information:
   - If critical info is missing, use sensible defaults
   - Default servings: 1 people
   - Default budget: ₹500 
   - Default cooking time: 45 minutes per meal
   - Default cuisine: Mixed/Varied

4. Output a clear, structured summary in this format:

IMPORTANT:
- If the user says they want something EVERY DAY (like egg daily), list it under DAILY MUST-HAVES in capitals
- This daily requirement must be passed forward so every agent respects it
- Do NOT lose any user requirements

Output ONLY the structured summary, nothing else"""


    return call_llm(system_prompt, user_input, agent_name='preference_analyzer')
