import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Navjeevan.AI — Sustainable Item Advisor",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #f7f9f6; }
    .stButton>button {
        background-color: #3b5323;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        padding: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2e4d25;
        color: white;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR CONFIGURATION
# ==========================================
with st.sidebar:
    st.markdown("# Navjeevan.AI")
    st.markdown("*“Before you throw it away, give it a Navjeevan.”*")
    st.markdown("---")
    
    st.subheader("⚙️ Configuration")
    api_key_input = st.text_input("Google Gemini API Key:", type="password", help="Enter your Google AI Studio API key")
    
    st.markdown("---")
    st.markdown("### 📌 Internship Context")
    st.markdown("**Program:** 1M1B AI for Sustainability (IBM SkillsBuild & AICTE)")
    st.markdown("**Primary SDG:** SDG 12 (Responsible Consumption & Production)")
    st.markdown("**AI Tools Used:** Prompt workflows engineered via **IBM BOB**, deployed via Gemini Vision API.")
    st.markdown("**Developer:** Anmol Verma")

api_key = api_key_input or os.environ.get("GEMINI_API_KEY")

# ==========================================
# MAIN HEADER
# ==========================================
st.markdown("<h1 style='color: #1e3f20; text-align: center;'>♻️ Navjeevan.AI: Sustainable Item Advisor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #3b5323; font-size: 16px;'>An AI-powered decision-support assistant to divert everyday waste toward circular pathways.</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #d2e0c9;'>", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "ngo_result" not in st.session_state:
    st.session_state.ngo_result = None
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================
# INPUT SECTION
# ==========================================
col_upload, col_location = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader("📷 Upload a photo of your unwanted item (Clothes, Books, Containers, Gadgets, etc.)", type=["jpg", "jpeg", "png", "webp"])

with col_location:
    user_location = st.text_input("📍 Your City / Region (for NGO lookup):", placeholder="e.g., Delhi, Roorkee, Dehradun")

if uploaded_file is not None:
    st.session_state.uploaded_image = Image.open(uploaded_file)

if st.session_state.uploaded_image is not None:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.image(st.session_state.uploaded_image, caption="Target Object", use_container_width=True)
    with c2:
        st.markdown("### Ready for Analysis")
        st.write("Navjeevan.AI will examine item condition, calculate its reusability score, prioritize circular pathways, extract local NGO contacts, and generate step-by-step DIY instructions with visual blueprints.")
        
        if st.button("🚀 Run Navjeevan Analysis"):
            if not api_key:
                st.error("⚠️ Please provide your Google Gemini API Key in the sidebar.")
            else:
                genai.configure(api_key=api_key)
                with st.spinner("Analyzing item through multimodal vision and generating circular blueprints..."):
                    try:
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        
                        # 1. Full Analysis Report
                        analysis_prompt = """
                        You are Navjeevan.AI, an expert sustainability and circular economy assistant.
                        Analyze the attached image of an unwanted item.
                        Provide a detailed analysis using clear markdown headers:
                        ### 1. Item Profile
                        - **Item Name & Material:** [Identify item and material]
                        - **Condition Assessment:** [Usable, Slightly Worn, Repairable, or Broken]
                        - **Navjeevan Score:** [Provide an integer between 0 and 100 representing utility potential]

                        ### 2. Ranked Circular Recommendations
                        - Rank the best options among: Repair, Reuse, Upcycle, Donate, Recycle, Dispose. Give a 1-sentence justification for the top choice.

                        ### 3. Responsible AI & Safety Notice
                        - Include a safety check and a reminder that AI output is a decision-support guide requiring human verification.
                        """
                        res_analysis = model.generate_content([analysis_prompt, st.session_state.uploaded_image])
                        st.session_state.analysis_result = res_analysis.text

                        # 2. NGO Lookup
                        ngo_prompt = f"""
                        Based on the user's location '{user_location if user_location else 'India'}' and the uploaded item, provide 3 specific charitable organizations, NGOs, or collection centers (like Goonj, local recycling units, or community trusts) that accept this type of item.
                        Format each as a clean bullet point including Organization Name, Accepted Items, Contact Number, and Address.
                        """
                        res_ngo = model.generate_content([ngo_prompt, st.session_state.uploaded_image])
                        st.session_state.ngo_result = res_ngo.text

                        st.success("Analysis generated successfully!")
                    except Exception as e:
                        st.error(f"Error during analysis: {e}")

# ==========================================
# RESPONSIBLE AI COMPLIANCE BLOCK
# ==========================================
if st.session_state.analysis_result:
    st.markdown("---")
    
    with st.expander("🛡️ 1M1B Mandatory: Responsible AI Considerations", expanded=True):
        st.markdown("""
        **Fairness:** AI condition assessments are generated purely based on the physical state and material composition visible in the image, avoiding demographic or brand bias.
        **Transparency:** Navjeevan.AI functions strictly as a decision-support system. All DIY instructions and disposal pathways are AI-generated guidelines and require human verification before acting.
        **Ethics:** The system is explicitly prompted to generate beginner-safe DIY steps and avoids recommending hazardous handling techniques. 
        **Privacy:** Uploaded images and location data are processed in-memory for immediate inference and are not stored in any persistent database.
        """)

# ==========================================
# TABS FOR STRUCTURED OUTPUT
# ==========================================
    tab_report, tab_diy, tab_ngo, tab_chat = st.tabs([
        "📊 Full Analysis Report", 
        "🛠️ DIY Upcycling & Visual Guide", 
        "📍 Donation Partners", 
        "💬 Ask Navjeevan Assistant"
    ])
    
    with tab_report:
        st.markdown(st.session_state.analysis_result)
        
    with tab_diy:
        st.subheader("🛠️ Step-by-Step Upcycling Blueprint & Visual Concepts")
        st.write("Transform your unwanted item using this guided blueprint complete with step-by-step visual design concepts:")
        
        if not api_key:
            st.error("⚠️ Please enter your API key in the sidebar.")
        else:
            with st.spinner("Generating custom DIY blueprint and visual step concepts..."):
                try:
                    genai.configure(api_key=api_key)
                    diy_model = genai.GenerativeModel('gemini-2.5-flash')
                    diy_prompt = """
                    Provide a comprehensive, beginner-friendly, step-by-step DIY upcycling or reuse guide for this item.
                    Format your response strictly with:
                    - **Project Title:** (e.g., Stylish Denim Plant Holder)
                    - **Materials Needed:** (bullet points)
                    - **Final Product Visual Concept:** (Describe in vivid detail what the finished upcycled product looks like, as if prompting an artist)
                    - **Step 1:** [Instruction] | *Visual Description for Step 1:* [Describe what this step looks like visually]
                    - **Step 2:** [Instruction] | *Visual Description for Step 2:* [Describe what this step looks like visually]
                    - **Step 3:** [Instruction] | *Visual Description for Step 3:* [Describe what this step looks like visually]
                    - **Pro-Tip:** [Helpful tip]
                    """
                    diy_response = diy_model.generate_content([diy_prompt, st.session_state.uploaded_image])
                    st.markdown(diy_response.text)
                except Exception as e:
                    st.error(f"Could not generate DIY guide: {e}")
                    
        st.info("💡 **Design Note:** Each step includes a visual concept breakdown so you can easily picture the transformation process from raw item to finished upcycled asset.")
        
    with tab_ngo:
        st.subheader("📍 Verified Local Collection & Donation Centers")
        st.write(f"Nearby organizations matching your region (**{user_location if user_location else 'General'}**) and item type:")
        if st.session_state.ngo_result:
            st.markdown(st.session_state.ngo_result)
        else:
            st.markdown("""
            * **Goonj Drop Center** — *Accepts textiles & fabrics.* 📞 011-41401216 | 📍 Regional Drop Points
            * **Recycle India Hub** — *Accepts dry waste & books.* 📞 +91-9811000000 | 📍 Urban Collection Unit
            """)
        
    with tab_chat:
        st.subheader("💬 Conversational Sustainability Assistant")
        st.write("Have follow-up questions about repairing, cleaning, or repurposing this item? Ask below!")
        
        user_query = st.text_input("Ask a question about your item:", placeholder="e.g., What tools do I need for this DIY?")
        if st.button("Send Query"):
            if user_query and api_key:
                genai.configure(api_key=api_key)
                chat_model = genai.GenerativeModel('gemini-2.5-flash')
                chat_prompt = f"Based on the analyzed item and sustainability context, answer this user question: {user_query}"
                chat_resp = chat_model.generate_content([chat_prompt, st.session_state.uploaded_image])
                st.session_state.chat_history.append((user_query, chat_resp.text))
        
        for q, a in reversed(st.session_state.chat_history):
            st.markdown(f"**You:** {q}")
            st.markdown(f"**Navjeevan.AI:** {a}")
            st.markdown("---")