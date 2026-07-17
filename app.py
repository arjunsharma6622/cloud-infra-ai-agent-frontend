# frontend/app.py
import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="AI Platform Assistant")
st.title("👷 AI Platform Engineering Assistant")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Split page into chat controls and generated asset panes
chat_col, output_col = st.columns([1, 1])

with chat_col:
    st.subheader("Conversation")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if prompt := st.chat_input("E.g., Build a production AKS environment..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        with st.spinner("Multi-agent graph executing..."):
            try:
                # Call FastAPI backend server
                response = requests.post("http://localhost:8000/chat", json={"prompt": prompt})
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.latest_result = result
                    st.success("Graph execution finished!")
                else:
                    st.error(f"Error {response.status_code} connecting to backend API.")
            except Exception as e:
                st.error(f"Failed to reach server: {e}")

with output_col:
    st.subheader("Generated Infrastructure Deliverables")
    
    if "latest_result" in st.session_state:
        res = st.session_state.latest_result
        
        tab1, tab2, tab3 = st.tabs(["1. Extracted Spec", "2. Architecture Plan", "3. Terraform Code"])
        
        with tab1:
            st.json(res.get("project_spec", {}))
            
        with tab2:
            st.markdown(res.get("architecture_plan", "No plan generated."))
            
        with tab3:
            code_files = res.get("generated_code", {})
            for filename, content in code_files.items():
                st.write(f"**`{filename}`**")
                st.code(content, language="hcl")
    else:
        st.info("Awaiting input to generate architecture artifacts.")