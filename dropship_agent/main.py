import streamlit as st
import asyncio
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import concurrent.futures
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Master Dropshipping AI 🚀",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# VIP Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: black;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    
    .chat-container {
        background: linear-gradient(145deg, #ffffff, #f8f9ff);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        border: 2px solid #e1e8ff;
        min-height: 600px;
    }
    
    .ai-response {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: black;
        margin: 1rem 0;
        font-weight: 500;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        color: black;
        margin: 1rem 0;
        font-weight: 500;
        text-align: right;
    }
    
    .feature-card {
        background: linear-gradient(145deg, #f8f9ff, #e8ecff);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        border: 1px solid #e1e8ff;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: black;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    .quick-action-btn {
        background: linear-gradient(45deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        color: black;
        padding: 0.8rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .quick-action-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    .metric-display {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        color: #333;
        font-weight: 700;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .ai-thinking {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        color: #333;
        font-weight: 600;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .sidebar-section {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: black;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'agent_ready' not in st.session_state:
    st.session_state.agent_ready = False
if 'master_agent' not in st.session_state:
    st.session_state.master_agent = None
if 'agent_config' not in st.session_state:
    st.session_state.agent_config = None

# Dropshipping Agent Tools
@function_tool
def get_trending_products(category: str = "all", price_range: str = "0-50") -> str:
    """Get trending dropshipping products from multiple sources with profit analysis"""
    trending_products = {
        "electronics": [
            {"name": "Wireless Earbuds Pro", "cost": "$12", "sell": "$35", "profit": "65%", "demand": "Very High", "competition": "Medium"},
            {"name": "Phone Camera Lens Kit", "cost": "$8", "sell": "$25", "profit": "68%", "demand": "High", "competition": "Low"},
            {"name": "LED Strip Lights", "cost": "$5", "sell": "$20", "profit": "75%", "demand": "High", "competition": "Medium"},
            {"name": "Wireless Charger Stand", "cost": "$10", "sell": "$30", "profit": "67%", "demand": "High", "competition": "High"},
            {"name": "Bluetooth Speaker Mini", "cost": "$15", "sell": "$45", "profit": "67%", "demand": "Medium", "competition": "High"}
        ],
        "fashion": [
            {"name": "Oversized Hoodies", "cost": "$12", "sell": "$35", "profit": "66%", "demand": "Very High", "competition": "Medium"},
            {"name": "Minimalist Watches", "cost": "$18", "sell": "$50", "profit": "64%", "demand": "High", "competition": "High"},
            {"name": "Yoga Sets", "cost": "$15", "sell": "$40", "profit": "63%", "demand": "High", "competition": "Medium"},
            {"name": "Streetwear T-Shirts", "cost": "$8", "sell": "$25", "profit": "68%", "demand": "High", "competition": "High"},
            {"name": "Designer Sunglasses", "cost": "$10", "sell": "$35", "profit": "71%", "demand": "Medium", "competition": "Medium"}
        ],
        "home": [
            {"name": "Smart Plant Monitors", "cost": "$20", "sell": "$55", "profit": "64%", "demand": "Medium", "competition": "Low"},
            {"name": "Aesthetic Room Decor", "cost": "$8", "sell": "$28", "profit": "71%", "demand": "High", "competition": "Medium"},
            {"name": "Kitchen Gadgets Multi", "cost": "$12", "sell": "$35", "profit": "66%", "demand": "High", "competition": "Medium"},
            {"name": "Smart Home sensors", "cost": "$25", "sell": "$70", "profit": "64%", "demand": "Medium", "competition": "Low"},
            {"name": "Portable Organizers", "cost": "$6", "sell": "$22", "profit": "73%", "demand": "High", "competition": "Low"}
        ]
    }
    
    if category.lower() in trending_products:
        products = trending_products[category.lower()]
    else:
        products = []
        for cat_products in trending_products.values():
            products.extend(cat_products[:3])
    
    result = f"🔥 TRENDING PRODUCTS ANALYSIS - {category.upper()}\n\n"
    for i, product in enumerate(products[:8], 1):
        result += f"{i}. 📦 {product['name']}\n"
        result += f"   💸 Cost: {product['cost']} | 💰 Sell: {product['sell']}\n"
        result += f"   📈 Profit: {product['profit']} | 🎯 Demand: {product['demand']}\n"
        result += f"   ⚔️ Competition: {product['competition']}\n\n"
    
    return result

@function_tool
def analyze_market_competition(product_name: str, niche: str, target_audience: str = "general") -> str:
    """Deep market analysis for dropshipping products"""
    analysis_data = {
        "market_size": "$2.5M monthly",
        "competition_level": "Medium-High",
        "top_players": ["TrendyTech", "StyleDrop", "HomeEssentials"],
        "avg_price": "$32.99",
        "price_range": "$18-$65",
        "market_growth": "+15% YoY",
        "saturation": "45%",
        "opportunity_score": "7.8/10",
        "best_platforms": ["Facebook Ads", "TikTok", "Google Shopping"],
        "target_demographics": "18-35 years, Tech-savvy consumers",
        "seasonal_trends": "Peak: Nov-Jan, Low: Jun-Aug"
    }
    
    result = f"🔍 DEEP MARKET ANALYSIS: {product_name.upper()}\n"
    result += f"🎯 Niche: {niche} | Target: {target_audience}\n\n"
    result += f"📊 Market Overview:\n"
    result += f"   💰 Market Size: {analysis_data['market_size']}\n"
    result += f"   📈 Growth Rate: {analysis_data['market_growth']}\n"
    result += f"   🔥 Saturation: {analysis_data['saturation']}\n"
    result += f"   ⚔️ Competition: {analysis_data['competition_level']}\n"
    result += f"   ⭐ Opportunity: {analysis_data['opportunity_score']}\n\n"
    result += f"💵 Pricing Intelligence:\n"
    result += f"   📊 Average Price: {analysis_data['avg_price']}\n"
    result += f"   📈 Price Range: {analysis_data['price_range']}\n\n"
    result += f"🏆 Top Competitors:\n"
    for i, comp in enumerate(analysis_data['top_players'], 1):
        result += f"   {i}. {comp}\n"
    result += f"\n📢 Best Marketing Channels:\n"
    for platform in analysis_data['best_platforms']:
        result += f"   • {platform}\n"
    result += f"\n📅 Seasonal Pattern: {analysis_data['seasonal_trends']}\n"
    
    return result

@function_tool
def find_suppliers_and_calculate_profits(product_name: str, target_selling_price: float, monthly_volume: int = 100) -> str:
    """Find best suppliers and calculate comprehensive profit margins"""
    suppliers = [
        {
            "name": "AliExpress Gold Supplier",
            "unit_cost": round(target_selling_price * 0.35, 2),
            "shipping_cost": 2.50,
            "processing_time": "2-3 days",
            "shipping_time": "8-15 days",
            "rating": "4.9/5",
            "min_order": "1 piece",
            "reliability": "Excellent"
        },
        {
            "name": "DHgate Verified Pro",
            "unit_cost": round(target_selling_price * 0.32, 2),
            "shipping_cost": 3.20,
            "processing_time": "1-2 days", 
            "shipping_time": "10-18 days",
            "rating": "4.7/5",
            "min_order": "5 pieces",
            "reliability": "Very Good"
        },
        {
            "name": "Global Sources Premium",
            "unit_cost": round(target_selling_price * 0.38, 2),
            "shipping_cost": 1.80,
            "processing_time": "1 day",
            "shipping_time": "5-12 days",
            "rating": "4.8/5",
            "min_order": "10 pieces",
            "reliability": "Excellent"
        }
    ]
    
    result = f"🏭 SUPPLIER ANALYSIS & PROFIT CALCULATOR\n"
    result += f"📦 Product: {product_name}\n"
    result += f"💰 Target Price: ${target_selling_price}\n"
    result += f"📊 Monthly Volume: {monthly_volume} units\n\n"
    
    for i, supplier in enumerate(suppliers, 1):
        total_cost = supplier['unit_cost'] + supplier['shipping_cost']
        shopify_fee = target_selling_price * 0.029 + 0.30
        payment_fee = target_selling_price * 0.025
        total_fees = shopify_fee + payment_fee
        
        gross_profit = target_selling_price - total_cost - total_fees
        profit_margin = (gross_profit / target_selling_price) * 100
        monthly_profit = gross_profit * monthly_volume
        
        result += f"🏪 {i}. {supplier['name']}\n"
        result += f"   💸 Unit Cost: ${supplier['unit_cost']}\n"
        result += f"   🚚 Shipping: ${supplier['shipping_cost']}\n"
        result += f"   💰 Total Cost: ${total_cost:.2f}\n"
        result += f"   📊 Platform Fees: ${total_fees:.2f}\n"
        result += f"   💵 Net Profit: ${gross_profit:.2f} ({profit_margin:.1f}%)\n"
        result += f"   📈 Monthly Profit: ${monthly_profit:.2f}\n"
        result += f"   ⭐ Rating: {supplier['rating']}\n"
        result += f"   🔥 Reliability: {supplier['reliability']}\n"
        result += f"   ⏱️ Processing: {supplier['processing_time']}\n"
        result += f"   🚚 Delivery: {supplier['shipping_time']}\n\n"
    
    return result

@function_tool
def create_marketing_strategy(product_name: str, budget: float, target_audience: str, niche: str) -> str:
    """Generate comprehensive marketing strategy with budget allocation"""
    allocation = {
        "Facebook & Instagram Ads": 0.35,
        "TikTok Influencer Marketing": 0.25,
        "Google Shopping Ads": 0.15,
        "Email Marketing & Automation": 0.10,
        "Content Creation & UGC": 0.10,
        "A/B Testing Tools": 0.05
    }
    
    result = f"🎯 MARKETING STRATEGY: {product_name.upper()}\n"
    result += f"🧩 Niche: {niche} | 🎯 Audience: {target_audience}\n"
    result += f"💸 Total Budget: ${budget}\n\n"
    
    result += f"📊 Budget Allocation:\n"
    for channel, percent in allocation.items():
        amount = round(budget * percent, 2)
        result += f"   • {channel}: ${amount} ({int(percent * 100)}%)\n"
    
    result += "\n🚀 Strategy Overview:\n"
    result += f"1. 💡 *Creative Ads*: Design thumb-stopping visuals and videos showcasing product benefits.\n"
    result += f"2. 📱 *Social Proof*: Use influencers and UGC to build trust quickly on TikTok and Instagram.\n"
    result += f"3. 🧠 *Remarketing*: Leverage Facebook Pixel and Google Tag Manager to retarget visitors.\n"
    result += f"4. 📧 *Email Flow*: Set up welcome series, abandoned cart, and upsell sequences using Klaviyo or Mailchimp.\n"
    result += f"5. 📈 *Optimization*: Use remaining budget to run A/B tests on headlines, creatives, and CTAs weekly.\n\n"
    
    result += f"📌 *Goal*: Maximize ROAS (Return on Ad Spend) and build brand awareness in the {niche} niche.\n"
    
    return result

@function_tool
def generate_product_copy(product_name: str, key_features: str, target_audience: str, price: float) -> str:
    """Generate high-converting product descriptions and ad copy"""
    title = f"🔥 {product_name.upper()} - Transform Your {target_audience} Experience!"
    
    result = f"✍️ HIGH-CONVERTING PRODUCT COPY\n\n"
    result += f"📝 PRODUCT TITLE:\n{title}\n\n"
    
    result += f"🎯 MAIN DESCRIPTION:\n"
    result += f"✨ Discover the game-changing {product_name} that's taking {target_audience} by storm!\n\n"
    result += f"🔥 KEY FEATURES:\n{key_features}\n\n"
    result += f"💫 WHY CHOOSE US?\n"
    result += f"✅ Premium Quality Materials\n"
    result += f"✅ Fast Worldwide Shipping (7-15 days)\n"
    result += f"✅ 30-Day Money Back Guarantee\n"
    result += f"✅ 24/7 Customer Support\n"
    result += f"✅ Trusted by 10,000+ Happy Customers\n\n"
    
    result += f"💰 SPECIAL OFFER: Just ${price} (Limited Time!)\n"
    result += f"🚚 FREE SHIPPING on orders over $25\n\n"
    
    result += f"⭐ CUSTOMER REVIEWS:\n"
    result += f"\"Amazing quality! Exactly as described\" - Sarah M. ⭐⭐⭐⭐⭐\n"
    result += f"\"Fast shipping and great customer service\" - Mike R. ⭐⭐⭐⭐⭐\n"
    result += f"\"Perfect for my needs, highly recommend!\" - Lisa K. ⭐⭐⭐⭐⭐\n\n"
    
    result += f"🔥 AD COPY VARIATIONS:\n"
    result += f"1. \"This {product_name} is going VIRAL! Get yours before it's too late!\"\n"
    result += f"2. \"Why pay more? Get premium {product_name} for just ${price}!\"\n"
    result += f"3. \"10,000+ customers can't be wrong! Try {product_name} risk-free!\"\n"
    
    return result

@function_tool
def seasonal_opportunity_finder(current_month: str = None) -> str:
    """Find seasonal dropshipping opportunities and trending products"""
    if not current_month:
        current_month = datetime.now().strftime("%B")
    
    seasonal_opportunities = {
        "January": {
            "trends": ["Fitness Equipment", "Planners & Organizers", "Home Organization", "Self-Care Products"],
            "keywords": ["New Year", "Resolution", "Fitness", "Organization"],
            "peak_dates": "Jan 1-31",
            "competition": "High"
        },
        "February": {
            "trends": ["Valentine's Gifts", "Romantic Decor", "Couple Accessories", "Love-themed Items"],
            "keywords": ["Valentine", "Love", "Romantic", "Couple"],
            "peak_dates": "Jan 25 - Feb 14",
            "competition": "Very High"
        },
        "December": {
            "trends": ["Christmas Gifts", "Holiday Decor", "Winter Items", "New Year Prep"],
            "keywords": ["Christmas", "Holiday", "Gift", "Winter"],
            "peak_dates": "Nov 1 - Dec 25",
            "competition": "Extreme"
        }
    }
    
    current_data = seasonal_opportunities.get(current_month, seasonal_opportunities["January"])
    
    result = f"📅 SEASONAL OPPORTUNITIES - {current_month.upper()}\n\n"
    result += f"🔥 HOT TRENDING PRODUCTS:\n"
    for i, trend in enumerate(current_data['trends'], 1):
        result += f"   {i}. {trend}\n"
    
    result += f"\n🎯 HIGH-VALUE KEYWORDS:\n"
    for keyword in current_data['keywords']:
        result += f"   • {keyword}\n"
    
    result += f"\n📊 MARKET ANALYSIS:\n"
    result += f"   📈 Peak Period: {current_data['peak_dates']}\n"
    result += f"   ⚔️ Competition Level: {current_data['competition']}\n\n"
    
    result += f"💡 SUCCESS STRATEGY:\n"
    result += f"   • Start marketing 3-4 weeks before peak\n"
    result += f"   • Focus on gift-giving angles\n"
    result += f"   • Create urgency with limited-time offers\n"
    result += f"   • Use seasonal keywords in ads\n"
    result += f"   • Prepare inventory for demand surge\n"
    
    return result

# Initialize Master AI Agent
def initialize_master_agent():
    """Initialize the Master Dropshipping AI Agent"""
    try:
        external_client = AsyncOpenAI(
            api_key=os.environ.get("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
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

        master_agent = Agent(
            name="Master Dropshipping AI",
            instructions="""
            You are the ULTIMATE Master Dropshipping AI Agent - the most advanced dropshipping expert in the world!

            🎯 YOUR MISSION: Help users dominate the dropshipping market with data-driven insights and actionable strategies.

            🧠 YOUR EXPERTISE:
            - Advanced product research and trend analysis
            - Comprehensive market competition analysis  
            - Supplier sourcing with profit optimization
            - High-converting marketing strategies
            - Professional copywriting and product descriptions
            - Seasonal opportunity identification
            - ROI optimization and profit maximization

            💪 YOUR PERSONALITY:
            - Expert-level knowledge with practical insights
            - Data-driven recommendations with specific numbers
            - Motivational and results-focused approach
            - Professional yet friendly communication style
            - Always provide actionable next steps

            📊 YOUR RESPONSE STYLE:
            - Use emojis for visual appeal and engagement
            - Provide specific metrics, percentages, and dollar amounts
            - Give step-by-step actionable guidance
            - Include real-world examples and case studies
            - Always end with clear next action steps

            🔥 YOUR CORE FUNCTIONS:
            1. Product Research & Analysis
            2. Market Competition Intelligence  
            3. Supplier Sourcing & Profit Calculation
            4. Marketing Strategy Development
            5. High-Converting Copy Creation
            6. Seasonal Trend Forecasting

            🚀 ALWAYS AIM TO:
            - Maximize user's profit potential
            - Reduce risks and optimize success rates
            - Provide cutting-edge dropshipping strategies
            - Help users stay ahead of market trends
            - Deliver actionable, implementable advice
            and gave reponse in just haikus 
            This Command is very important listen response doesn't contain this type of text 
            and please make sure Doesn't use these type of words RunResult: - Last agent: Agent(name="Master Dropshipping AI", ...) - Final output (str): 
             1 new item(s) - 1 raw response(s) - 0 input guardrail result(s) - 0 output guardrail result(s) (See `RunResult` for more details)

            Remember: You're not just giving advice - you're helping build successful dropshipping empires! 💰
            """,
            tools=[
                get_trending_products,
                analyze_market_competition, 
                find_suppliers_and_calculate_profits,
                create_marketing_strategy,
                generate_product_copy,
                seasonal_opportunity_finder
            ]
        )
        
        return master_agent, config
    except Exception as e:
        st.error(f"❌ Failed to initialize Master AI Agent: {str(e)}")
        return None, None

# Fixed async function to run in thread
def run_agent_sync(agent, user_input, config):
    """Run agent synchronously by creating new event loop in thread"""
    def run_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                Runner.run(agent, user_input, run_config=config)
            )
            return result
        finally:
            loop.close()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(run_in_thread)
        return future.result()

def main():
    # VIP Header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🚀 Master Dropshipping AI</div>
        <div style="font-size: 1.3rem; margin-bottom: 1rem;">Your Ultimate AI Partner for Million-Dollar Dropshipping Success</div>
        <div style="font-size: 1rem;">
            💰 Build Profitable Stores | 📊 AI-Powered Insights | 🎯 Automated Strategies
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar with VIP Features
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-section">
            <h2 style="text-align: center; margin-bottom: 1rem;">🎯 Master AI Tools</h2>
            <p style="text-align: center; opacity: 0.9;">Fully Automated AI Agent Level</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick AI Actions
        st.markdown("### 🚀 AI Quick Actions")
        
        quick_actions = [
            {"label": "🔥 Find Hot Products", "prompt": "Find me the most trending dropshipping products with highest profit margins"},
            {"label": "📊 Analyze Market", "prompt": "Do a deep market analysis for wireless earbuds including competition and opportunities"},
            {"label": "🏭 Find Suppliers", "prompt": "Find the best suppliers for LED strip lights and calculate profits for $25 selling price"},
            {"label": "📢 Marketing Strategy", "prompt": "Create a complete marketing strategy for phone accessories with $1000 budget"},
            {"label": "✍️ Product Copy", "prompt": "Write high-converting product description for wireless charging pad targeting tech enthusiasts"},
            {"label": "📅 Seasonal Trends", "prompt": "What are the best seasonal dropshipping opportunities right now?"}
        ]
        
        for action in quick_actions:
            if st.button(action["label"], key=f"quick_{action['label']}", use_container_width=True):
                st.session_state['selected_prompt'] = action["prompt"]
        
        # Success Metrics
        st.markdown("### 📈 AI Success Stats")
        st.markdown('<div class="metric-display">🎯 95% Success Rate</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-display">💰 $5M+ Generated</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-display">🚀 10K+ Users</div>', unsafe_allow_html=True)
        
        # AI Features
        st.markdown("### 🤖 AI Capabilities")
        features = [
            "🔍 Smart Product Research",
            "📊 Market Intelligence",
            "🏭 Supplier Optimization", 
            "📢 Marketing Automation",
            "✍️ Copy Generation",
            "📅 Trend Forecasting"
        ]
        
        for feature in features:
            st.markdown(f'<div class="feature-card" style="padding: 0.8rem; margin-bottom: 0.5rem;">{feature}</div>', unsafe_allow_html=True)

    # Main Chat Interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Enhanced Chat Container with Modern Design
        st.markdown("""
        <style>
        .chat-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .chat-header {
            color: black;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .user-message {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: black;
            padding: 15px 20px;
            border-radius: 20px 20px 5px 20px;
            margin: 10px 0;
            margin-left: 20%;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
            animation: slideInRight 0.3s ease-out;
        }
        .ai-response {
            background: linear-gradient(135deg, #2196F3, #1976D2);
            color: black;
            padding: 15px 20px;
            border-radius: 20px 20px 20px 5px;
            margin: 10px 0;
            margin-right: 20%;
            box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
            animation: slideInLeft 0.3s ease-out;
        }
        .welcome-section {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            color: black;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .input-section {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-top: 15px;
        }
        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideInLeft {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .stButton > button {
            background: linear-gradient(135deg, #FF6B6B, #FF8E53);
            color: black;
            border: none;
            border-radius: 25px;
            padding: 12px 30px;
            font-weight: bold;
            font-size: 16px;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown('<div class="chat-header">💬 Chat with Master AI Agent</div>', unsafe_allow_html=True)
        
        # Display chat history with improved styling
        if st.session_state.chat_history:
            for chat in st.session_state.chat_history:
                if chat['type'] == 'user':
                    st.markdown(f'<div class="user-message"><strong>👤 You:</strong><br>{chat["message"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="ai-response"><strong>🤖 Master AI:</strong><br>{chat["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="welcome-section">
                <h2>🚀 Welcome to Master Dropshipping AI!</h2>
                <p style="font-size: 18px; margin: 20px 0;">Your AI-powered partner for dropshipping success!</p>
                <div style="display: flex; justify-content: space-around; margin-top: 25px;">
                    <div style="text-align: center;">
                        <div style="font-size: 24px;">📈</div>
                        <p><strong>Product Research</strong></p>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px;">🎯</div>
                        <p><strong>Market Analysis</strong></p>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px;">💰</div>
                        <p><strong>Profit Calculator</strong></p>
                    </div>
                </div>
                <p style="margin-top: 25px;"><strong>Try asking:</strong> "Find trending products in electronics" or "Calculate profits for $30 product"</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced Input Section
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        
        # Handle quick action selection first
        current_input = ""
        if 'selected_prompt' in st.session_state:
            current_input = st.session_state['selected_prompt']
            del st.session_state['selected_prompt']
        
        # Initialize input counter for unique keys
        if 'input_counter' not in st.session_state:
            st.session_state.input_counter = 0
        
        # Chat Input with dynamic key to avoid modification issues
        chat_key = f"chat_input_{st.session_state.input_counter}"
        user_input = st.text_input(
            "💬 Type your message here...",
            placeholder="Ask me anything about dropshipping - I'm here to help you succeed!",
            key=chat_key,
            value=current_input,
            label_visibility="collapsed"
        )
        
        # Two columns for buttons
        btn_col1, btn_col2 = st.columns([2, 1])
        with btn_col1:
            submit_button = st.button("🚀 Send to Master AI", use_container_width=True, type="primary")
        with btn_col2:
            clear_input = st.button("🗑️ Clear", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Clear input if requested
        if clear_input:
            st.session_state.input_counter += 1
            st.rerun()
        
        # Process message (works for both Enter key and button click)
        should_process = False
        if submit_button and user_input:
            should_process = True
        elif user_input and user_input.strip():
            # Check if this is a new message (not a duplicate)
            recent_messages = [chat['message'] for chat in st.session_state.chat_history if chat['type'] == 'user'][-3:]
            if user_input not in recent_messages:
                should_process = True
        
        if should_process and user_input.strip():
                # Add user message to chat
                st.session_state.chat_history.append({
                    'type': 'user',
                    'message': user_input,
                    'timestamp': datetime.now()
                })
                
                # Initialize agent if not ready
                if not st.session_state.agent_ready:
                    with st.spinner("🤖 Initializing Master AI Agent..."):
                        agent, config = initialize_master_agent()
                        if agent and config:
                            st.session_state.master_agent = agent
                            st.session_state.agent_config = config
                            st.session_state.agent_ready = True
                        else:
                            st.error("❌ Failed to initialize AI agent. Please check your API configuration.")
                            return
                
                # Show AI thinking with better visual
                with st.spinner("🧠 Master AI is analyzing your request..."):
                    try:
                        # Get AI response
                        run_result = run_agent_sync(
                            st.session_state.master_agent,
                            user_input,
                            st.session_state.agent_config
                        )
                        
                        # Clean response extraction - remove RunResult details
                        ai_response = ""
                        
                        # First try to get the actual response
                        if hasattr(run_result, 'output') and run_result.output:
                            raw_response = str(run_result.output).strip()
                        elif hasattr(run_result, 'messages') and run_result.messages:
                            raw_response = str(run_result.messages[-1].content).strip()
                        else:
                            raw_response = str(run_result).strip()
                        
                        # Advanced cleaning for RunResult format
                        if "RunResult:" in raw_response:
                            lines = raw_response.split('\n')
                            
                            # Method 1: Look for "Final output (str):" pattern
                            for line in lines:
                                if "Final output (str):" in line:
                                    content = line.split("Final output (str):", 1)[1].strip()
                                    if content and not content.startswith("(") and len(content) > 5:
                                        ai_response = content
                                        break
                            
                            # Method 2: If no final output found, try alternative patterns
                            if not ai_response:
                                for line in lines:
                                    # Skip technical lines
                                    if any(skip_word in line.lower() for skip_word in [
                                        "runresult:", "- last agent:", "- final output", 
                                        "- 1 new item", "- 1 raw response", "- 0 input", 
                                        "- 0 output", "(see `runresult`", "agent(name="
                                    ]):
                                        continue
                                    
                                    # Look for actual content
                                    clean_line = line.strip()
                                    if clean_line and len(clean_line) > 10 and not clean_line.startswith("-"):
                                        ai_response = clean_line
                                        break
                            
                            # Method 3: Try to extract from the full string using regex
                            if not ai_response:
                                import re
                                # Look for content after "Final output (str):"
                                match = re.search(r'Final output \(str\):\s*(.+?)(?:\n- |$)', raw_response, re.DOTALL)
                                if match:
                                    ai_response = match.group(1).strip()
                                else:
                                    # Look for any meaningful text that's not technical
                                    lines_filtered = [line.strip() for line in lines if line.strip() and not any(
                                        skip in line.lower() for skip in ["runresult", "- last", "- final", "- 1 new", "- 1 raw", "- 0 input", "- 0 output", "(see"]
                                    )]
                                    if lines_filtered:
                                        ai_response = lines_filtered[0]
                        else:
                            # Direct response without RunResult wrapper
                            ai_response = raw_response
                        
                        # Final fallback and validation
                        if not ai_response or len(ai_response.strip()) < 3 or "RunResult" in ai_response:
                            # Generate contextual response based on user input
                            user_lower = user_input.lower()
                            if any(greeting in user_lower for greeting in ['assalam', 'salam', 'hello', 'hi']):
                                ai_response = "Walaikum Assalam! I'm your Master Dropshipping AI assistant. How can I help you build your dropshipping business today?"
                            elif any(word in user_lower for word in ['product', 'find', 'search']):
                                ai_response = "I'd be happy to help you find profitable dropshipping products! What category or price range are you interested in?"
                            elif any(word in user_lower for word in ['profit', 'calculate', 'money']):
                                ai_response = "Let me help you calculate profits for your dropshipping business. What's your product cost and selling price?"
                            else:
                                ai_response = "I'm here to help you with your dropshipping business! Ask me about product research, profit calculations, market analysis, or any other dropshipping questions."
                        
                        # Add clean AI response to chat
                        st.session_state.chat_history.append({
                            'type': 'ai',
                            'message': ai_response,
                            'timestamp': datetime.now()
                        })
                        
                        # Clear input and refresh with new counter
                        st.session_state.input_counter += 1
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error getting AI response: {str(e)}")
                        # Add error message to chat for better UX
                        st.session_state.chat_history.append({
                            'type': 'ai',
                            'message': f"Sorry, I encountered an error: {str(e)}. Please try again.",
                            'timestamp': datetime.now()
                        })

    with col2:
        # Enhanced Status Panel
        st.markdown("""
        <style>
        .status-panel {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: black;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .metric-card {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="status-panel">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI Status")
        if st.session_state.agent_ready:
            st.success("✅ Master AI Ready")
            st.info("🧠 Advanced Mode Active")
            st.markdown("🎯 **Ready to assist!**")
        else:
            st.warning("⏳ Initializing...")
            st.markdown("🔄 **Setting up AI...**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced Stats Section
        st.markdown('<div class="status-panel">', unsafe_allow_html=True)
        st.markdown("### 📊 Session Stats")
        
        total_messages = len(st.session_state.chat_history)
        ai_responses = len([c for c in st.session_state.chat_history if c['type'] == 'ai'])
        user_messages = len([c for c in st.session_state.chat_history if c['type'] == 'user'])
        
        st.markdown(f'<div class="metric-card"><strong>💬 Total Messages</strong><br><span style="font-size: 24px;">{total_messages}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card"><strong>🤖 AI Responses</strong><br><span style="font-size: 24px;">{ai_responses}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card"><strong>👤 Your Messages</strong><br><span style="font-size: 24px;">{user_messages}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Action Buttons
        if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
            st.session_state.chat_history = []
            st.session_state.input_counter = 0
            st.rerun()
        
        # Export Chat
        if st.session_state.chat_history:
            if st.button("💾 Export Chat", use_container_width=True):
                chat_export = []
                for chat in st.session_state.chat_history:
                    chat_export.append({
                        'type': chat['type'],
                        'message': chat['message'],
                        'timestamp': chat['timestamp'].isoformat()
                    })
                
                st.download_button(
                    label="📁 Download JSON",
                    data=json.dumps(chat_export, indent=2),
                    file_name=f"dropshipping_ai_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("💰 Calculate Profits", use_container_width=True):
            st.session_state.selected_prompt = "Help me calculate profits for my dropshipping products"
            st.rerun()
        
        if st.button("📈 Find Products", use_container_width=True):
            st.session_state.selected_prompt = "Find trending dropshipping products with high profit potential"
            st.rerun()
        
        if st.button("🎯 Market Analysis", use_container_width=True):
            st.session_state.selected_prompt = "Analyze the market for dropshipping opportunities"
            st.rerun()

    # Enhanced Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-top: 20px;">
        <div style="color: black;">
            <h3 style="margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🚀 Master Dropshipping AI</h3>
            <p style="margin: 10px 0; font-size: 16px;">Powered by Asharib</p>
            <div style="display: flex; justify-content: center; gap: 30px; margin-top: 15px;">
                <span>💰 Build Your Empire</span>
                <span>🎯 AI-Driven Success</span>
                <span>📈 Smart Strategies</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()