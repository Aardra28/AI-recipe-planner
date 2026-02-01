def analyze_preferences(user_input: str, call_llm) -> str:
    """
    Agent 1: Analyzes user preferences and extracts structured information
    
    Args:
        user_input: Natural language input from user
        call_llm: Function to call the LLM
        
    Returns:
        Structured preference summary
    """
    system_prompt = """You are a Preference Analyzer agent for a recipe management system.

Your task is to:
1. Read the user's natural language input carefully
2. Extract the following information:
   - Number of people/servings
   - Dietary preferences (vegetarian, vegan, non-veg, pescatarian, etc.)
   - Specific proteins they eat (chicken, fish, lamb, etc.)
   - Allergies and food restrictions (shellfish, nuts, dairy, gluten, etc.)
   - Preferred cuisines (Indian, Italian, Chinese, Kerala, Mediterranean, etc.)
   - Budget constraints (in ₹ or $)
   - Cooking time limits (max time willing to spend)
   - Any other special preferences (spicy level, cooking methods, etc.)

3. Validate the information:
   - If critical info is missing, use sensible defaults
   - Default servings: 2 people
   - Default budget: ₹5,000 per week
   - Default cooking time: 45 minutes per meal
   - Default cuisine: Mixed/Varied

4. Output a clear, structured summary in this format:

## PREFERENCE SUMMARY

**👥 Servings:** [number] people

**🍽️ Dietary Type:** [type]

**✅ Allowed Proteins:** [list]

**❌ Restrictions/Allergies:** [list]

**🌍 Preferred Cuisines:** [list]

**💰 Weekly Budget:** ₹[amount]

**⏱️ Max Cooking Time:** [time] minutes

**🌶️ Other Preferences:** [any additional notes]

Be thorough, accurate, and fill in reasonable defaults for any missing information.
Output ONLY the structured summary, nothing else."""

    return call_llm(system_prompt, user_input, agent_name='preference_analyzer')