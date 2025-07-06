import os
import csv
import requests
import time
import streamlit as st
from apify_client import ApifyClient

# ==============================
# Configuration - Set your API keys here
# ==============================
SERPER_API_KEY = "eb9ae17edabdbea0cc19b557e7d3ed911f0d87c3"
APIFY_TOKEN = "apify_api_rouSIEu4Gte5bhmBaNRIKgcIkTyp3Y15eei0"

# Initialize Apify Client
apify_client = ApifyClient(APIFY_TOKEN)

# ==============================
# Tool Definitions
# ==============================
def scrape_google_maps_places(query: str, limit: int = 10) -> list:
    """Scrape business listings from Google Maps using Serper.dev API"""
    st.session_state.messages.append({"role": "system", "content": f"🔍 Starting Google Maps search for: '{query}'"})
    
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "gl": "pk"}
    
    try:
        # Add retry mechanism for timeout issues
        for attempt in range(3):  # Retry up to 3 times
            try:
                response = requests.post(
                    "https://google.serper.dev/places", 
                    headers=headers, 
                    json=payload,
                    timeout=40  # Increased timeout
                )
                response.raise_for_status()
                break  # Break out of retry loop if successful
            except requests.exceptions.Timeout:
                if attempt < 2:  # Not the last attempt
                    wait_time = (attempt + 1) * 5  # Exponential backoff
                    st.session_state.messages.append({"role": "system", "content": f"⏳ Timeout occurred, retrying in {wait_time} seconds..."})
                    time.sleep(wait_time)
                    continue
                else:
                    raise  # Re-raise exception on last attempt
        
        results = response.json().get("places", [])
        if not results:
            st.session_state.messages.append({"role": "system", "content": "⚠️ No results found on Google Maps"})
            return []
            
        leads = []
        for item in results[:limit]:
            leads.append({
                "Source": "Google Maps",
                "Name": item.get("title", "N/A"),
                "Address": item.get("address", "N/A"),
                "Phone": item.get("phoneNumber", "N/A"),
                "Rating": item.get("rating", "N/A"),
                "Description": item.get("description", "N/A")
            })
            
        st.session_state.messages.append({"role": "system", "content": f"✅ Found {len(leads)} Google Maps leads"})
        return leads
        
    except Exception as e:
        error_msg = f"❌ Google Maps error: {str(e)}"
        st.session_state.messages.append({"role": "system", "content": error_msg})
        return [{"Error": error_msg}]

def scrape_linkedin_profiles(query: str, max_results: int = 10) -> list:
    """Scrape LinkedIn profiles using Apify Actor"""
    ACTOR_ID = "pocesar~linkedin-company-employees-scraper"
    st.session_state.messages.append({"role": "system", "content": f"🔍 Starting LinkedIn search for: '{query}'"})
    
    # Prepare actor input
    run_input = {
        "queries": [query],
        "maxResults": max_results,
        "proxyConfig": {"useApifyProxy": True}
    }
    
    try:
        st.session_state.messages.append({"role": "system", "content": "🚀 Starting Apify actor run..."})
        run = apify_client.actor(ACTOR_ID).call(run_input=run_input)
        
        st.session_state.messages.append({"role": "system", "content": "⏳ Fetching results from dataset..."})
        dataset_items = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
        
        if not dataset_items:
            st.session_state.messages.append({"role": "system", "content": "⚠️ No LinkedIn profiles found"})
            return []
            
        # Format results
        leads = []
        for profile in dataset_items[:max_results]:
            leads.append({
                "Source": "LinkedIn",
                "Name": profile.get("fullName", "N/A"),
                "Position": profile.get("position", "N/A"),
                "Company": profile.get("companyName", "N/A"),
                "Location": profile.get("location", "N/A"),
                "Profile URL": profile.get("url", "N/A")
            })
            
        success_msg = f"✅ Found {len(leads)} LinkedIn profiles"
        st.session_state.messages.append({"role": "system", "content": success_msg})
        st.session_state.messages.append({"role": "system", "content": f"💾 Dataset URL: https://console.apify.com/storage/datasets/{run['defaultDatasetId']}"})
        return leads
        
    except Exception as e:
        error_msg = f"❌ LinkedIn scraping error: {str(e)}"
        st.session_state.messages.append({"role": "system", "content": error_msg})
        return [{"Error": error_msg}]

def export_leads_to_csv(leads: list) -> str:
    """Export leads to CSV file. Creates new file or appends to existing one."""
    if not leads:
        return "❌ No leads to export"
    
    filename = "leads.csv"
    file_exists = os.path.isfile(filename)
    
    try:
        # Get all possible fieldnames from existing file and new leads
        fieldnames = set()
        if file_exists:
            with open(filename, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames:
                    fieldnames.update(reader.fieldnames)
        
        for lead in leads:
            fieldnames.update(lead.keys())
        
        # Write to CSV
        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=sorted(fieldnames))
            
            if not file_exists or f.tell() == 0:
                writer.writeheader()
                
            writer.writerows(leads)
            
        success_msg = f"✅ {len(leads)} leads saved to {filename}"
        st.session_state.messages.append({"role": "system", "content": success_msg})
        return success_msg
        
    except Exception as e:
        error_msg = f"❌ CSV export error: {str(e)}"
        st.session_state.messages.append({"role": "system", "content": error_msg})
        return error_msg

# ==============================
# Formatting Functions
# ==============================
def format_leads_for_display(leads):
    """Format leads into a beautiful, easy-to-copy text format"""
    if not leads or not isinstance(leads, list):
        return "No leads to display"
    
    formatted = ""
    for i, lead in enumerate(leads, 1):
        formatted += f"🔹 Lead #{i}\n"
        for key, value in lead.items():
            formatted += f"  • {key}: {value}\n"
        formatted += "\n"
    return formatted

def display_leads_in_ui(leads):
    """Display leads in a beautiful format in Streamlit UI"""
    if not leads:
        st.warning("No leads to display")
        return
    
    st.subheader("✨ Scraped Leads")
    for i, lead in enumerate(leads, 1):
        with st.container():
            st.markdown(f"##### 🔹 Lead #{i}")
            for key, value in lead.items():
                st.markdown(f"**{key}:** {value}")
            st.divider()

# ==============================
# Streamlit UI
# ==============================
def main():
    st.set_page_config(
        page_title="LeadScraper Pro",
        page_icon="🔍",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "leads" not in st.session_state:
        st.session_state.leads = []
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    # Custom CSS for styling
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #ffffff;
        border: 1px solid #dddddd;
        border-radius: 8px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stButton>button:disabled {
        background-color: #cccccc;
    }
    .message {
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
        font-size: 16px;
    }
    .system {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
    }
    .success {
        background-color: #e8f5e9;
        border-left: 4px solid #4CAF50;
    }
    .error {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    .title {
        color: #1a73e8;
        text-align: center;
        margin-bottom: 30px;
    }
    .disclaimer {
        background-color: #fff8e1;
        border-left: 4px solid #ffc107;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .credit-warning {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # App header
    st.markdown('<h1 class="title">🔍 LeadScraper Pro</h1>', unsafe_allow_html=True)
    st.caption("Extract business leads from Google Maps and LinkedIn with AI-powered scraping")
    
    # IMPORTANT DISCLAIMER
    st.markdown("""
    <div class="disclaimer">
        <strong>⚠️ IMPORTANT NOTICE:</strong>
        <ul>
            <li>This tool is currently running in <strong>FREE MODE</strong> with limited API credits</li>
            <li>Please do not scrape more than 10 leads at a time</li>
            <li>All leads are authentic but limited to 10 per search due to API constraints</li>
            <li>If you encounter errors, it may be due to exhausted credits</li>
            <li>Please use responsibly and avoid excessive scraping</li>
        </ul>
    </div>
    
    <div class="credit-warning">
        <strong>🛑 CREDIT LIMIT WARNING:</strong>
        <ul>
            <li>This free version is limited to 20 leads per day</li>
            <li>Errors usually indicate exhausted API credits</li>
            <li>For professional use, consider upgrading to a paid plan</li>
            <li>We are honest people providing authentic leads within limits</li>
            <li>Please don't abuse the system - شكريا (Thank you)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Always show download button if CSV exists
    if os.path.exists("leads.csv"):
        with open("leads.csv", "rb") as f:
            st.sidebar.download_button(
                label="📥 Download Leads CSV",
                data=f,
                file_name="leads.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Input form
    with st.form("scraper_form", clear_on_submit=False):
        col1, col2 = st.columns([3, 1])
        with col1:
            query = st.text_input("Search Query", placeholder="e.g., 'dentists in Lahore' or 'textile companies'")
        with col2:
            source = st.selectbox("Source", ["Google", "LinkedIn"])
        
        submitted = st.form_submit_button(
            "🚀 Get Leads", 
            disabled=st.session_state.processing,
            use_container_width=True
        )
    
    # Display messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        if role == "system":
            if "✅" in content or "💾" in content:
                st.markdown(f'<div class="message success">{content}</div>', unsafe_allow_html=True)
            elif "❌" in content or "Error" in content:
                st.markdown(f'<div class="message error">{content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message system">{content}</div>', unsafe_allow_html=True)
    
    # Display leads in beautiful format
    if st.session_state.leads:
        display_leads_in_ui(st.session_state.leads)
        
        # Copy-friendly text area
        with st.expander("📝 Copy Leads as Text", expanded=True):
            lead_text = format_leads_for_display(st.session_state.leads)
            st.text_area("Easy to copy format:", value=lead_text, height=300, key="copy_area")
            st.caption("Select all text and copy (Ctrl+C / Cmd+C)")
    
    # Process form submission
    if submitted and not st.session_state.processing:
        if not query:
            st.error("Please enter a search query")
            return
            
        # Clear previous messages and leads for new run
        st.session_state.messages = []
        st.session_state.leads = []
        st.session_state.processing = True
        
        # Add initial message
        st.session_state.messages.append({"role": "system", "content": f"🚀 Starting {source} scraping for: '{query}'"})
        
        # Execute scraping directly (no agent)
        with st.spinner(f"🔍 Scraping {source} leads. This may take a moment..."):
            try:
                if source == "Google":
                    # Scrape Google Maps
                    leads = scrape_google_maps_places(query, limit=10)
                    
                    # Export to CSV
                    export_result = export_leads_to_csv(leads)
                    st.session_state.messages.append({"role": "system", "content": export_result})
                    
                    # Store leads for display
                    st.session_state.leads = leads
                    
                elif source == "LinkedIn":
                    # Scrape LinkedIn
                    leads = scrape_linkedin_profiles(query, max_results=10)
                    
                    # Export to CSV
                    export_result = export_leads_to_csv(leads)
                    st.session_state.messages.append({"role": "system", "content": export_result})
                    
                    # Store leads for display
                    st.session_state.leads = leads
                
                st.session_state.messages.append({"role": "system", "content": "🏁 Scraping completed!"})
                
                # Format leads for final display
                formatted_leads = format_leads_for_display(leads)
                st.session_state.messages.append({"role": "system", "content": f"✨ Formatted Leads:\n{formatted_leads}"})
                
            except Exception as e:
                error_msg = f"❌ Error during scraping: {str(e)}"
                st.session_state.messages.append({"role": "system", "content": error_msg})
                
                # Add credit exhaustion message
                if "quota" in str(e).lower() or "credit" in str(e).lower():
                    st.session_state.messages.append({
                        "role": "system", 
                        "content": "🛑 API credits exhausted. Please try again tomorrow or upgrade your plan."
                    })
            finally:
                st.session_state.processing = False
        
        # Force rerun to update UI
        st.rerun()

if __name__ == "__main__":
    main()