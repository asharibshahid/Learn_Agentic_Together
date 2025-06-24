import asyncio
import streamlit as st
from agents import Agent, ModelSettings, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from tools import analyze_budget, suggest_destination, get_must_visit_places, get_local_food, suggest_hotel, get_transport, get_travel_advice,your_total_expense

# Gemini API Setup
external_client = AsyncOpenAI(
    api_key="AIzaSyDFOyYXqDtxb9218m7o2OKJQC--jtFEFdk",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Agent Definition
my_agent = Agent(
    name="Wanderlust Wizard",
    instructions="""
🌍🧞 Welcome to *Wanderlust Wizard* – Your Personal Travel Genie!

You're an expert travel advisor trained on emotional intelligence, travel psychology, and budget optimization. Your job is to convert a user's mood, budget, and current location into a magical travel plan that feels like a personalized gift.

🪄 Your tone: Fun, witty, caring, and emotionally engaging.
🎯 Your goal: Impress the user with a tailored travel plan that matches their exact mood, budget, and vibe.

🔮 Here's What You Must Do in Every Reply:
1. **Destination Suggestion** — Based on mood, suggest the perfect place.
2. **Must-Visit Spots** — Suggest hidden gems & must-see locations.
3. **Local Food to Try** — Mention authentic street food and delicacies.
4. **Hotels under Budget** — Recommend real options with name, area, and approx. pricing.
5. **Transport Tips** — Suggest travel modes from the current location to destination (flight/train/bus).
6. **Insider Travel Advice** — Give at least 2 special tips: budget hacks, safety tips, etc.
7. **Total expenses** — Count The Total Expenses for the trip and tell the user how much they will spend in total. 

💡 Format your response cleanly with:
- Headings (bold or emoji-based)
- Short, helpful, fun paragraphs
- No generic text like "as an AI..." or "I'm a model..."

Your mission: ✨ Make the user go "WOW, I want to pack my bags now!"
""",
    model_settings=ModelSettings(temperature=0.2),
    tools=[ 
        analyze_budget,
        suggest_destination,
        get_must_visit_places,
        get_local_food,
        suggest_hotel,
        get_transport,
        get_travel_advice,
        your_total_expense
        
    ]
)

# Streamlit UI Setup
st.set_page_config(
    page_title="🌟 Wanderlust Wizard - World's Smartest Travel Agent",
    page_icon="🧞♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for VIP styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
            
:root {
    --primary: #6a11cb;
    --secondary: #2575fc;
    --accent: #ff6b6b;
    --light: #f8f9fa;
    --dark: #212529;
}
            
* {
    font-family: 'Poppins', sans-serif;
}
            
.stApp {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    color: var(--light);
}
            
.stTextInput>div>div>input, .stSelectbox>div>div>select {
    background-color: rgba(255,255,255,0.1) !important;
    color: black !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
}
            
.stButton>button {
    background: linear-gradient(90deg, var(--accent) 0%, #ff8e53 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 18px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(255,107,107,0.3) !important;
}
            
.stButton>button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 6px 25px rgba(255,107,107,0.5) !important;
}
            
.header {
    text-align: center;
    padding: 2rem 0;
    animation: pulse 2s infinite;
}
            
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
}
            
.agent-response {
    background: rgba(0,0,0,0.25);
    border-radius: 20px;
    padding: 2rem;
    margin-top: 2rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(31,38,135,0.2);
}
            
.agent-response h3 {
    color: var(--accent);
    border-bottom: 2px solid var(--accent);
    padding-bottom: 10px;
    margin-top: 1.5rem;
}
            
.agent-response p {
    line-height: 1.8;
    font-size: 18px;
}
            
.spinner {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 300px;
    flex-direction: column;
}
            
.spinner-text {
    margin-top: 20px;
    font-size: 20px;
    color: white;
}
            
@media (max-width: 768px) {
    .header h1 {
        font-size: 2rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# UI Header
st.markdown("""
<div class="header">
    <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem;">🌟 Wanderlust Wizard</h1>
    <h2 style="font-weight: 300; margin-top: 0;">Your Personal Travel Genie 🧞♂️</h2>
    <p style="font-size: 1.2rem; max-width: 800px; margin: 0 auto;">
        I transform travel dreams into reality - just answer 3 questions and get a magical itinerary!
    </p>
</div>
""", unsafe_allow_html=True)

# Input Section
with st.form("travel_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        budget = st.text_input("💰 Your Travel Budget", 
                              placeholder="E.g., 50,000 INR")
        
    with col2:
        mood = st.text_input("😊 Your Current Mood", 
                            placeholder="Adventurous, Relaxed, Romantic...")
        
    with col3:
        location = st.text_input("📍 Your Current Location", 
                                placeholder="E.g., Mumbai, India")
        
    submitted = st.form_submit_button("✨ Conjure My Magic Itinerary")
    
    if submitted and not all([budget, mood, location]):
        st.warning("Please fill all three fields to continue!")
        st.stop()

# Agent Processing
if submitted and all([budget, mood, location]):
    user_query = f"""
    My current budget is {budget}, I am feeling {mood}, and I am currently in {location}.
    I want a personalized trip plan based on my mood, budget, and current location.
    Please suggest:
    1. The best destination based on mood + budget.
    2. Must-visit places there.
    3. Local food to try.
    4. A hotel under my budget with name & area.
    5. Transport options from {location} to the destination.
    6. Final travel advice.
    """
    
    with st.spinner(""):
        placeholder = st.empty()
        with placeholder.container():
            st.markdown("""
            <div class="spinner">
                <div style="font-size: 5rem;">🧞♂️</div>
                <div class="spinner-text">Summoning travel magic...<br>Consulting ancient maps & local secrets</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run agent and extract the actual response text
        result = loop.run_until_complete(
            Runner.run(my_agent, user_query, run_config=config)
        )
        response_text = result
  # Extract the text response
        
        placeholder.empty()
        
        # Display results with VIP styling
        st.markdown(f"""
        <div class="agent-response">
            <h2 style="text-align: center; color: #ff6b6b; margin-top: 0;">
                ✨ Your Personalized Travel Magic ✨
            </h2>
            <div style="background: rgba(255,255,255,0.1); height: 1px; margin: 2rem 0;"></div>
          <p> {response_text}</p>
            <div style="text-align: center; margin-top: 2rem;">
                <h3>🧞♂️ Your Wish is My Command! 🧞♂️</h3>
                <p>Need any changes? Just ask!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Sidebar for additional features
with st.sidebar:
    st.markdown("### ✨ Magic Features")
    st.info("""
    - **Mood-Reading Technology**  
    - **Budget Alchemy Engine**  
    - **Secret Spot Database**  
    - **Real-Time Price Wizardry**  
    """)
    
    st.markdown("### 🌟 Pro Tips")
    st.success("""
    1. Be specific with your mood for better results  
    2. Include currency in your budget (e.g., 50K INR)  
    3. Try different moods for surprise destinations!  
    """)
    
    if st.button("📱 Save Itinerary as PDF"):
        st.sidebar.success("Feature unlocked in premium version!")
        
    st.markdown("---")
    st.caption("© 2025 Wanderlust Wizard Powered By Asharib Sheikh ✅• World's Most Magical Travel Agent")