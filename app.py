import streamlit as st
from PIL import Image
import os
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from elevenlabs.client import ElevenLabs

# Load environment variables from .env file
load_dotenv()

# Import all agent functions
from preference_analyzer import analyze_preferences
from recipe_searcher import search_recipes
from recipe_analyzer import analyze_recipes
from meal_plan_composer import compose_meal_plan
from nutritional_analyst import analyze_nutrition
from markdown_formatter import format_markdown


# ============================================================================
# MODEL CONFIGURATION
# ============================================================================
MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"
TEMPERATURE = 1

# Token limits for each agent to avoid rate limiting
MAX_TOKENS = {
    'preference_analyzer': 2000,
    'recipe_searcher': 3000,
    'recipe_analyzer': 4000,
    'meal_plan_composer': 3000,
    'nutritional_analyst': 3000,
    'markdown_formatter': 4000
}


def call_llm(system_prompt: str, user_input: str, agent_name: str = 'default') -> str:
    """
    Call LLM with system and user inputs
    
    Args:
        system_prompt: System prompt defining agent behavior
        user_input: Input for the agent
        agent_name: Name of the agent (for token limit lookup)
        
    Returns:
        Complete response from the LLM
    """
    client = Groq()  # Uses GROQ_API_KEY from environment
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    
    print('messages-test', messages)
    # Get max tokens for this agent, default to 3000 if not specified
    max_tokens = MAX_TOKENS.get(agent_name, 3000)
    
    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=max_tokens,
        top_p=1,
        stream=False,
        stop=None
    )
    
    response_text = completion.choices[0].message.content
    print('test-call_llm- return', response_text)
    return response_text


@st.cache_resource
def get_elevenlabs_client():
    """Initialize ElevenLabs client for speech-to-text"""
    api_key = os.getenv("api_key")  # Make sure this matches your .env variable name
    if not api_key:
        st.error("⚠️ ElevenLabs API key not found. Please set 'api_key' in your .env file.")
        return None
    return ElevenLabs(api_key=api_key)


def transcribe_audio(audio_file):
    """
    Transcribe audio file using ElevenLabs
    
    Args:
        audio_file: Audio file from st.audio_input
        
    Returns:
        Transcribed text or None if error
    """
    try:
        elevenlabs = get_elevenlabs_client()
        if elevenlabs is None:
            st.error("❌ ElevenLabs client not initialized")
            return None
        
        print(f"Audio file type: {type(audio_file)}")
        print(f"Audio file: {audio_file}")
        
        # Reset file pointer to beginning
        audio_file.seek(0)
            
        transcription = elevenlabs.speech_to_text.convert(
            file=audio_file,
            model_id="scribe_v2",
        )
        
        print(f"Transcription result: {transcription}")
        print(f"Transcription text: {transcription.text}")
        
        if transcription and transcription.text:
            return transcription.text
        else:
            st.error("❌ No text returned from transcription")
            return None
            
    except Exception as e:
        st.error(f"❌ Transcription error: {str(e)}")
        print(f"Full error: {e}")
        import traceback
        traceback.print_exc()
        return None


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="AI Recipe Management System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"  # Show sidebar with image
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4ECDC4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-section {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #FF6B6B;
    }
    .success-message {
        color: #00C851;
        font-weight: bold;
    }
    .error-message {
        color: #ff4444;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #FF6B6B;
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #FF5252;
    }
    /* Microphone button styling */
    div[data-testid="column"]:last-child button {
        font-size: 1.5rem;
        height: 50px;
        margin-top: 8px;
    }
    </style>
    """, unsafe_allow_html=True)


def load_image():
    """Load and display the header image"""
    try:
        # Use raw string (r"") or forward slashes for Windows paths
        image_path = "download.jpg"
        
        if os.path.exists(image_path):
            image = Image.open(image_path)
            return image
        else:
            st.warning(f"Image not found at: {image_path}")
            return None
    except Exception as e:
        st.warning(f"Could not load image: {str(e)}")
        return None
    

def run_multi_agent_pipeline(user_input: str):
    """
    Run the complete multi-agent pipeline
    
    Args:
        user_input: User's meal planning request
        
    Returns:
        Dictionary containing all agent outputs and final result
    """
    
    results = {
        'preferences': None,
        'recipes': None,
        'recipe_analysis': None,
        'meal_plan': None,
        'nutritional_analysis': None,
        'final_output': None,
        'errors': []
    }
    
    try:
        # Agent 1: Preference Analyzer
        with st.spinner("🔍 Agent 1: Analyzing your preferences..."):
            print('-----------------------------------------------------------------')
            print("")
            print('test', user_input)
            print('test', call_llm)
            results['preferences'] = analyze_preferences(user_input, call_llm)
            st.success("✅ Preferences analyzed successfully!")
            print('check- results', results)
            print('check- results_preferences', results['preferences'])
            
            
        # Agent 2: Recipe Searcher
        with st.spinner("🔎 Agent 2: Searching for recipes..."):
            results['recipes'] = search_recipes(results['preferences'], call_llm)
            st.success("✅ Recipes found successfully!")
        
        # Agent 3: Recipe Analyzer
        with st.spinner("📊 Agent 3: Analyzing recipes in detail..."):
            results['recipe_analysis'] = analyze_recipes(results['recipes'], call_llm)
            st.success("✅ Recipe analysis completed!")
        
        # Agent 4: Meal Plan Composer
        with st.spinner("📅 Agent 4: Composing your meal plan..."):
            results['meal_plan'] = compose_meal_plan(results['recipe_analysis'], call_llm)
            st.success("✅ Meal plan created successfully!")
        
        # Agent 5: Nutritional Analyst
        with st.spinner("🥗 Agent 5: Analyzing nutrition..."):
            results['nutritional_analysis'] = analyze_nutrition(results['meal_plan'], call_llm)
            st.success("✅ Nutritional analysis completed!")
        
        # Agent 6: Markdown Formatter
        with st.spinner("✨ Agent 6: Formatting your final meal plan..."):
            all_data = {
                'preferences': results['preferences'],
                'recipes': results['recipes'],
                'recipe_analysis': results['recipe_analysis'],
                'meal_plan': results['meal_plan'],
                'nutritional_analysis': results['nutritional_analysis']
            }
            results['final_output'] = format_markdown(all_data, call_llm)
            st.success("✅ Final meal plan ready!")
        
    except Exception as e:
        error_msg = f"Error occurred: {str(e)}"
        results['errors'].append(error_msg)
        st.error(f"⚠️ {error_msg}")
    
    return results


def main():
    """Main Streamlit application"""
    
    # Sidebar with image
    with st.sidebar:
        image = load_image()
        if image:
            st.image(image, use_column_width=True)
    
    # Title
    st.markdown('<p class="main-header">🍽️ AI Recipe Management System</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your Personalized Meal Planner</p>', unsafe_allow_html=True)
    
    # Main content area
    st.markdown("---")
    
    # User input section
    st.subheader("📝 Tell us about your meal preferences")
    
    # Initialize session state
    if 'transcribed_text' not in st.session_state:
        st.session_state.transcribed_text = ""
    
    # Text input area
    typed_text = st.text_area(
        "",
        height=150,
        placeholder="Type your preferences here... OR use the microphone below",
        key="typed_input",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Voice input
    st.info("🎤 Or click the microphone and speak your preferences")
    audio_file = st.audio_input("Record your voice")
    
    if audio_file is not None:
        with st.spinner("🎧 Transcribing your voice..."):
            transcribed = transcribe_audio(audio_file)
            
            if transcribed:
                st.session_state.transcribed_text = transcribed
                st.success("✅ Voice transcribed successfully!")
    
    # Determine which input to use
    if st.session_state.transcribed_text:
        st.markdown("### 📝 Your transcribed preferences:")
        st.info(st.session_state.transcribed_text)
        user_input = st.session_state.transcribed_text
    elif typed_text.strip():
        user_input = typed_text
    else:
        user_input = ""
    
    # Generate button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button("🚀 Generate My Meal Plan", use_container_width=True)
    
    # Process when button is clicked
    if generate_button:
        if not user_input.strip():
            st.warning("⚠️ Please enter your meal preferences (type or speak) before generating a plan.")
        else:
            # Run the pipeline
            st.markdown("---")
            st.subheader("🤖 AI Agents Working...")
            
            results = run_multi_agent_pipeline(user_input)
            
            # Display results
            if results['final_output'] and not results['errors']:
                st.markdown("---")
                st.markdown("## 🎉 Your Personalized Meal Plan is Ready!")
                
                # Create tabs for different views
                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                    "📋 Final Plan",
                    "👤 Preferences",
                    "🔍 Recipes",
                    "📊 Analysis",
                    "📅 Meal Plan",
                    "🥗 Nutrition"
                ])
                
                with tab1:
                    st.markdown(results['final_output'])
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Meal Plan (Markdown)",
                        data=results['final_output'],
                        file_name=f"meal_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                
                with tab2:
                    st.markdown('<div class="agent-section">', unsafe_allow_html=True)
                    st.markdown("### Agent 1: Preference Analysis")
                    st.markdown(results['preferences'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with tab3:
                    st.markdown('<div class="agent-section">', unsafe_allow_html=True)
                    st.markdown("### Agent 2: Recipe Search Results")
                    st.markdown(results['recipes'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with tab4:
                    st.markdown('<div class="agent-section">', unsafe_allow_html=True)
                    st.markdown("### Agent 3: Detailed Recipe Analysis")
                    st.markdown(results['recipe_analysis'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with tab5:
                    st.markdown('<div class="agent-section">', unsafe_allow_html=True)
                    st.markdown("### Agent 4: Meal Plan")
                    st.markdown(results['meal_plan'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with tab6:
                    st.markdown('<div class="agent-section">', unsafe_allow_html=True)
                    st.markdown("### Agent 5: Nutritional Analysis")
                    st.markdown(results['nutritional_analysis'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
            elif results['errors']:
                st.error("⚠️ Errors occurred during processing:")
                for error in results['errors']:
                    st.error(f"❌ {error}")
    



if __name__ == "__main__":
    main()
