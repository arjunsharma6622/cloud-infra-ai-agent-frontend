import streamlit as st
import requests
import json
import uuid

# --- PAGE CONFIG MUST BE THE FIRST COMMAND ---
st.set_page_config(layout="centered", page_title="AI Platform Assistant")

# --- CUSTOM CSS ---
custom_css = """
<style>
    header { visibility: hidden !important; }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 950px !important; 
    }
    footer { visibility: hidden !important; }
    [data-testid="stBottomBlockContainer"] { padding-bottom: 1rem !important; }
    [data-testid="stChatInput"] { padding-bottom: 0rem !important; }

    /* PROMPT CARD STYLES */
    .prompt-card {
        position: relative;
        background-color: #f7f7f8;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 12px 16px 28px 16px; 
        margin-bottom: 0.5rem;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    @media (prefers-color-scheme: dark) {
        .prompt-card {
            background-color: #212121;
            border-color: #333333;
            color: #ececec;
        }
    }
    .prompt-toggle { display: none; }
    .prompt-text {
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
        line-height: 1.5;
        font-size: 0.95rem;
        word-break: break-word;
    }
    .prompt-toggle:checked ~ .prompt-text {
        display: block;
        overflow: visible;
    }
    .expand-btn {
        position: absolute;
        bottom: 6px;
        right: 12px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 0.78rem;
        font-weight: 500;
        color: #666;
        cursor: pointer;
        user-select: none;
        padding: 3px 6px;
        border-radius: 6px;
        transition: background-color 0.2s, color 0.2s;
    }
    .expand-btn:hover { background-color: rgba(0, 0, 0, 0.06); color: #111; }
    @media (prefers-color-scheme: dark) {
        .expand-btn { color: #999; }
        .expand-btn:hover { background-color: rgba(255, 255, 255, 0.1); color: #fff; }
    }
    .chevron-icon {
        width: 14px;
        height: 14px;
        fill: currentColor;
        transition: transform 0.2s ease;
    }
    .prompt-toggle:checked ~ .expand-btn .chevron-icon { transform: rotate(180deg); }
    .prompt-toggle:not(:checked) ~ .expand-btn .btn-text::after { content: "Show more"; }
    .prompt-toggle:checked ~ .expand-btn .btn-text::after { content: "Show less"; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
st.title("Infra AI Agent")


# --- HELPER: RENDER USER PROMPT ---
def render_user_prompt(text: str, max_lines: int = 3):
    unique_id = f"prompt-{uuid.uuid4().hex[:8]}"
    if len(text) < 150:
        html_code = f'<div class="prompt-card"><div class="prompt-text" style="-webkit-line-clamp: unset;">{text}</div></div>'
    else:
        html_code = f"""
        <div class="prompt-card">
            <input type="checkbox" id="{unique_id}" class="prompt-toggle" />
            <div class="prompt-text" style="-webkit-line-clamp: {max_lines};">{text}</div>
            <label for="{unique_id}" class="expand-btn">
                <span class="btn-text"></span>
                <svg class="chevron-icon" viewBox="0 0 24 24"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6z"/></svg>
            </label>
        </div>
        """
    st.markdown(html_code, unsafe_allow_html=True)


# --- MODAL DIALOGS ---
# These functions open pop-ups when called via button clicks.
@st.dialog("Parsed Intent (JSON)", width="large")
def show_json_modal(spec_data):
    st.json(spec_data)

@st.dialog("Software Requirements Specification (SRS)", width="large")
def show_srs_modal(srs_data):
    st.markdown(srs_data)

@st.dialog("Architecture Blueprint", width="large")
def show_archi_modal(plan_data):
    # Ensure plan_data is rendered as markdown properly
    if isinstance(plan_data, list) and len(plan_data) > 0 and isinstance(plan_data[0], dict):
        plan_data = plan_data[0].get("text", str(plan_data))
    st.markdown(plan_data)


# --- HELPER: RENDER ASSISTANT OUTPUT ---
def render_assistant_output(msg_id, summary, spec, srs, plan, code):
    # 1. Summary
    st.markdown(summary)
    
    # 2. Artifact Buttons (Using columns to display them nicely side-by-side)
    # Buttons require unique keys so Streamlit knows which one is clicked in history
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if spec and st.button("{ } Intent Parser", key=f"btn_json_{msg_id}", use_container_width=True):
            show_json_modal(spec)
    with col2:
        if srs and st.button("📄 SRS Sheet", key=f"btn_srs_{msg_id}", use_container_width=True):
            show_srs_modal(srs)
    with col3:
        if plan and st.button("🏗️ Architecture", key=f"btn_archi_{msg_id}", use_container_width=True):
            show_archi_modal(plan)
            
    st.write("") # small spacing

    # 3. Final Code (Updated to use Accordions/Expanders)
    if code:
        st.markdown("#### Generated Infrastructure Files")
        for fname, content in code.items():
            # Create an accordion for each file
            with st.expander(f"💻 {fname}"):
                clean_content = content.replace("\\n", "\n").replace("\\t", "  ")
                st.code(clean_content, language="hcl")


# --- STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []


# --- STEP 1: RENDER CHAT HISTORY ---
for idx, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        with st.chat_message("user"):
            render_user_prompt(msg["content"], max_lines=3)
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            render_assistant_output(
                msg_id=idx,
                summary=msg.get("summary", ""),
                spec=msg.get("spec", {}),
                srs=msg.get("srs", ""),
                plan=msg.get("plan", ""),
                code=msg.get("code", {})
            )


# --- STEP 2: PROCESS NEW INPUT ---
if prompt := st.chat_input("E.g., Build an Azure environment with isolated networks..."):
    
    # 1. Save and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        render_user_prompt(prompt, max_lines=3)

    # 2. Assistant Processing
    with st.chat_message("assistant"):
        final_spec, final_plan, final_code, final_srs = {}, "", {}, ""
        
        # --- DYNAMIC LOADING TEXT ---
        # st.empty() creates a placeholder we can overwrite instantly
        status_text = st.empty()
        status_text.markdown("⏳ Parsing user requirements...")
        
        try:
            response = requests.post("http://localhost:8000/stream", json={"prompt": prompt}, stream=True)
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    
                    if "intent_parser" in chunk:
                        status_text.markdown("📝 Generating SRS document...")
                        final_spec = chunk["intent_parser"].get("project_spec", {})
                        # MOCKING SRS DATA for demonstration
                        final_srs = "### 1. Introduction\nThis document outlines the cloud infrastructure requirements...\n\n### 2. Networking\n- Virtual Network setup..."
                            
                    elif "architecture_planner" in chunk:
                        status_text.markdown("🏗️ Designing architecture topology...")
                        final_plan = chunk["architecture_planner"].get("architecture_plan", "")
                            
                    elif "iac_generator" in chunk:
                        status_text.markdown("💻 Writing Terraform Code...")
                        final_code = chunk["iac_generator"].get("generated_code", {})
                                
                    elif "validation_agent" in chunk:
                        val_data = chunk["validation_agent"]
                        if not val_data.get("validation_passed"):
                            status_text.markdown("⚠️ Fixing syntax errors in generated code...")
            
            # Clear the loading text when completely done
            status_text.empty()
            
        except Exception as e:
            status_text.markdown(f"❌ **Execution Aborted:** {e}")

        # --- RENDER FINAL OUTPUT ---
        if final_code:
            summary = "✅ **Infrastructure generated successfully.** Based on your requirements, I've designed the architecture and provisioned the necessary code below. Click the buttons to view the reasoning artifacts."
            
            # Generate a unique ID for the current message's buttons
            msg_id = len(st.session_state.messages)
            
            # Render the UI natively
            render_assistant_output(msg_id, summary, final_spec, final_srs, final_plan, final_code)
            
            # Save everything to state so it persists in the loop above
            st.session_state.messages.append({
                "role": "assistant",
                "summary": summary,
                "spec": final_spec,
                "srs": final_srs,
                "plan": final_plan,
                "code": final_code
            })