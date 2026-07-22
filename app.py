# # frontend/app.py
# import streamlit as st
# import requests
# import json

# st.set_page_config(layout="wide", page_title="AI Platform Assistant")
# st.title("👷 AI Platform Engineering Assistant")

# # Initialize session state for messages and streaming cache
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # --- STEP 1: DEFINE LAYOUT COLUMNS ---
# chat_col, output_col = st.columns([1, 1])

# # --- STEP 2: INITIALIZE THE TAB PLACEHOLDERS FIRST (Prevents NameError) ---
# with output_col:
#     st.subheader("Generated Infrastructure Deliverables")
#     tab1, tab2, tab3 = st.tabs(["1. Extracted Spec", "2. Architecture Plan", "3. Terraform Code"])
    
#     with tab1:
#         spec_placeholder = st.empty()
#     with tab2:
#         plan_placeholder = st.empty()
#     with tab3:
#         code_placeholder = st.empty()

# # --- STEP 3: RENDER HISTORICAL CACHED DATA IF AVAILABLE ---
# if "latest_spec" in st.session_state:
#     spec_placeholder.json(st.session_state.latest_spec)
# if "latest_plan" in st.session_state:
#     # Safely extract text block from Gemini content list if needed
#     plan_data = st.session_state.latest_plan
#     if isinstance(plan_data, list) and len(plan_data) > 0 and isinstance(plan_data[0], dict):
#         plan_data = plan_data[0].get("text", str(plan_data))
#     plan_placeholder.markdown(plan_data)
# if "latest_code" in st.session_state:
#     with code_placeholder.container(height=400):
#         for filename, content in st.session_state.latest_code.items():
#             st.write(f"**`{filename}`**")
#             st.code(content.replace("\\n", "\n"), language="hcl", line_numbers=True)

# # --- STEP 4: CHAT CONVERSATION PROCESSING INTERFACE ---
# with chat_col:
#     st.subheader("Conversation")
    
#     # Display previous messages
#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])
            
#     # Process new prompt inputs
#     if prompt := st.chat_input("E.g., Build an Azure environment with isolated networks..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.write(prompt)
            
#         with st.status("🧠 Agents are thinking...", expanded=True) as status:
#             try:
#                 # Initiate the streaming HTTP call to the FastAPI network endpoint
#                 response = requests.post("http://localhost:8000/stream", json={"prompt": prompt}, stream=True)
                
#                 for line in response.iter_lines():
#                     if line:
#                         chunk = json.loads(line.decode("utf-8"))
                        
#                         # Capture intent parser outputs
#                         if "intent_parser" in chunk:
#                             status.write("✅ **Intent Parser** extracted requirements.")
#                             spec_data = chunk["intent_parser"].get("project_spec", {})
#                             st.session_state.latest_spec = spec_data
#                             spec_placeholder.json(spec_data)
                            
#                         # Capture architecture planner outputs
#                         elif "architecture_planner" in chunk:
#                             status.write("✅ **Architecture Planner** designed the topology.")
#                             plan_data = chunk["architecture_planner"].get("architecture_plan", "")
#                             st.session_state.latest_plan = plan_data
                            
#                             # Safely parse text list array format if returned by Gemini client
#                             if isinstance(plan_data, list) and len(plan_data) > 0 and isinstance(plan_data[0], dict):
#                                 plan_data = plan_data[0].get("text", str(plan_data))
#                             plan_placeholder.markdown(plan_data)
                            
#                         # Capture terraform code output streams
#                         elif "iac_generator" in chunk:
#                             status.write("✅ **IaC Generator** wrote the Terraform code.")
#                             code_data = chunk["iac_generator"].get("generated_code", {})
#                             st.session_state.latest_code = code_data
                            
#                             code_placeholder.empty()
#                             with code_placeholder.container(height=400):
#                                 for filename, content in code_data.items():
#                                     st.write(f"**`{filename}`**")
#                                     st.code(content.replace("\\n", "\n"), language="hcl", line_numbers=True)
                                    
#                         # Capture validation logs
#                         elif "validation_agent" in chunk:
#                             val_data = chunk["validation_agent"]
#                             if val_data.get("validation_passed"):
#                                 status.write("✅ **Validation Agent** verified code syntax successfully.")
#                             else:
#                                 err = val_data.get('validation_errors', '')
#                                 status.write(f"⚠️ **Validation Agent** caught syntax anomalies! Routing back for fixing...")
#                                 status.write(f"```\n{err}\n```")
                
#                 status.update(label="Execution Complete!", state="complete", expanded=False)
#                 st.rerun() # Refresh layout to cleanly persist the historical state boxes
                
#             except Exception as e:
#                 status.update(label="Execution Aborted", state="error")
#                 st.error(f"Failed to process graph stream workflow: {e}")




# frontend/app.py
# import streamlit as st
# import requests
# import json

# st.set_page_config(layout="wide", page_title="AI Platform Assistant")
# st.title("Infra AI Agent")

# # Initialize session state for messages and streaming cache
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # --- STEP 1: DEFINE LAYOUT COLUMNS ---
# chat_col, output_col = st.columns([1, 1])

# # --- STEP 2: INITIALIZE THE TAB PLACEHOLDERS FIRST (Prevents NameError) ---
# with output_col:
#     st.subheader("Generated Infrastructure Deliverables")
#     tab1, tab2, tab3 = st.tabs(["1. Extracted Spec", "2. Architecture Plan", "3. Terraform Code"])
    
#     with tab1:
#         spec_placeholder = st.empty()
#     with tab2:
#         plan_placeholder = st.empty()
#     with tab3:
#         code_placeholder = st.empty()

# # --- STEP 3: RENDER HISTORICAL CACHED DATA IF AVAILABLE ---
# if "latest_spec" in st.session_state:
#     spec_placeholder.json(st.session_state.latest_spec)

# if "latest_plan" in st.session_state:
#     plan_data = st.session_state.latest_plan
#     if isinstance(plan_data, list) and len(plan_data) > 0 and isinstance(plan_data[0], dict):
#         plan_data = plan_data[0].get("text", str(plan_data))
#     plan_placeholder.markdown(plan_data)
    
# if "latest_code" in st.session_state:
#     # PLACEMENT 1: Fixed code editor height box for the historical views
#     with code_placeholder.container(height=500):
#         for filename, content in st.session_state.latest_code.items():
#             st.markdown(f"### 📄 `{filename}`")
#             clean_content = content.replace("\\n", "\n").replace("\\t", "  ")
#             st.code(clean_content, language="hcl", line_numbers=True)

# # --- STEP 4: CHAT CONVERSATION PROCESSING INTERFACE ---
# with chat_col:
#     st.subheader("Conversation")
    
#     # Display previous messages
#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])
            
#     # Process new prompt inputs
#     if prompt := st.chat_input("E.g., Build an Azure environment with isolated networks..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.write(prompt)
            
#         with st.status("🧠 Agents are thinking...", expanded=True) as status:
            # try:
            #     # Initiate the streaming HTTP call to the FastAPI network endpoint
            #     response = requests.post("http://localhost:8000/stream", json={"prompt": prompt}, stream=True)
                
            #     for line in response.iter_lines():
            #         if line:
            #             chunk = json.loads(line.decode("utf-8"))
                        
            #             # Capture intent parser outputs
            #             if "intent_parser" in chunk:
            #                 status.write("✅ **Intent Parser** extracted requirements.")
            #                 spec_data = chunk["intent_parser"].get("project_spec", {})
            #                 st.session_state.latest_spec = spec_data
            #                 spec_placeholder.json(spec_data)
                            
            #             # Capture architecture planner outputs
            #             elif "architecture_planner" in chunk:
            #                 status.write("✅ **Architecture Planner** designed the topology.")
            #                 plan_data = chunk["architecture_planner"].get("architecture_plan", "")
            #                 st.session_state.latest_plan = plan_data
                            
            #                 if isinstance(plan_data, list) and len(plan_data) > 0 and isinstance(plan_data[0], dict):
            #                     plan_data = plan_data[0].get("text", str(plan_data))
            #                 plan_placeholder.markdown(plan_data)
                            
            #             # Capture terraform code output streams
            #             elif "iac_generator" in chunk:
            #                 status.write("✅ **IaC Generator** wrote the Terraform code.")
            #                 code_data = chunk["iac_generator"].get("generated_code", {})
            #                 st.session_state.latest_code = code_data
                            
            #                 # PLACEMENT 2: Fixed code editor height box for live incoming streams
            #                 code_placeholder.empty()
            #                 with code_placeholder.container(height=500):
            #                     for filename, content in code_data.items():
            #                         st.markdown(f"### 📄 `{filename}`")
            #                         clean_content = content.replace("\\n", "\n").replace("\\t", "  ")
            #                         st.code(clean_content, language="hcl", line_numbers=True)
                                    
            #             # Capture validation logs
            #             elif "validation_agent" in chunk:
            #                 val_data = chunk["validation_agent"]
            #                 if val_data.get("validation_passed"):
            #                     status.write("✅ **Validation Agent** verified code syntax successfully.")
            #                 else:
            #                     err = val_data.get('validation_errors', '')
            #                     status.write(f"⚠️ **Validation Agent** caught syntax anomalies! Routing back for fixing...")
            #                     status.write(f"```\n{err}\n```")
                
            #     status.update(label="Execution Complete!", state="complete", expanded=False)
            #     st.rerun() # Refresh layout to cleanly persist the historical state boxes
                
            # except Exception as e:
            #     status.update(label="Execution Aborted", state="error")
            #     st.error(f"Failed to process graph stream workflow: {e}")


# frontend/app.py
# import streamlit as st
# import requests
# import json

# st.set_page_config(layout="wide", page_title="AI Platform Assistant")
# st.title("Infra AI Agent")

# # Initialize session state for messages and streaming cache
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "is_streaming" not in st.session_state:
#     st.session_state.is_streaming = False

# # --- STEP 1: DEFINE LAYOUT COLUMNS ---
# chat_col, output_col = st.columns([1, 1])

# # --- STEP 2: INITIALIZE THE LIVE VIEWPORT ---
# with output_col:
#     st.subheader("Generated Infrastructure Deliverables")
#     # This single placeholder acts as our TV screen during the live stream
#     live_viewport = st.empty()

# # --- STEP 3: RENDER HISTORICAL TABS (ONLY WHEN NOT STREAMING) ---
# if not st.session_state.is_streaming and "latest_spec" in st.session_state:
#     # Render the tabs inside the viewport once everything is done
#     with live_viewport.container():
#         tab1, tab2, tab3 = st.tabs(["1. Extracted Spec", "2. Architecture Plan", "3. Terraform Code"])
        
#         with tab1:
#             st.json(st.session_state.latest_spec)
            
#         with tab2:
#             plan_data = st.session_state.latest_plan
#             if isinstance(plan_data, list) and len(plan_data) > 0 and isinstance(plan_data[0], dict):
#                 plan_data = plan_data[0].get("text", str(plan_data))
#             st.markdown(plan_data)
            
#         with tab3:
#             with st.container(height=500):
#                 for filename, content in st.session_state.latest_code.items():
#                     st.markdown(f"### 📄 `{filename}`")
#                     clean_content = content.replace("\\n", "\n").replace("\\t", "  ")
#                     st.code(clean_content, language="hcl", line_numbers=True)

# # --- STEP 4: CHAT CONVERSATION PROCESSING INTERFACE ---
# with chat_col:
#     st.subheader("Conversation")
    
#     # Display previous messages
#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])
            
#     # Process new prompt inputs
#     if prompt := st.chat_input("E.g., Build an Azure environment with isolated networks..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
        
#         # Lock the UI into streaming mode to hide the tabs
#         st.session_state.is_streaming = True 
        
#         with st.chat_message("user"):
#             st.write(prompt)
            
#         with st.status("🧠 Agents are thinking...", expanded=True) as status:
#             try:
#                 response = requests.post("http://localhost:8000/stream", json={"prompt": prompt}, stream=True)
#                 #security

#                 # 🔒 Guardrail response handling
#                 if response.headers.get("content-type") == "application/json":
#                     data = response.json()
#                     if data.get("status") == "blocked":
#                         st.error(data["message"])
#                         st.session_state.is_streaming = False
#                         st.stop()
#                 for line in response.iter_lines():
#                     if line:
#                         chunk = json.loads(line.decode("utf-8"))
                        
#                         # --- 1. INTENT PARSER FINISHES ---
#                         if "intent_parser" in chunk:
#                             status.write("✅ **Intent Parser** extracted requirements.")
#                             spec_data = chunk["intent_parser"].get("project_spec", {})
#                             st.session_state.latest_spec = spec_data
                            
#                             # Instantly flash the JSON to the right screen
#                             with live_viewport.container():
#                                 st.info("👀 **Focus Mode:** Extracting Specification...")
#                                 st.json(spec_data)
                                
#                         # --- 2. ARCHITECTURE PLANNER FINISHES ---
#                         elif "architecture_planner" in chunk:
#                             status.write("✅ **Architecture Planner** designed the topology.")
#                             plan_data = chunk["architecture_planner"].get("architecture_plan", "")
#                             st.session_state.latest_plan = plan_data
                            
#                             if isinstance(plan_data, list) and len(plan_data) > 0 and isinstance(plan_data[0], dict):
#                                 plan_data = plan_data[0].get("text", str(plan_data))
                                
#                             # Instantly overwrite the right screen with the Markdown Plan
#                             with live_viewport.container():
#                                 st.info("👀 **Focus Mode:** Drafting Architecture Plan...")
#                                 st.markdown(plan_data)
                                
#                         # --- 3. IAC GENERATOR FINISHES ---
#                         elif "iac_generator" in chunk:
#                             status.write("✅ **IaC Generator** wrote the Terraform code.")
#                             code_data = chunk["iac_generator"].get("generated_code", {})
#                             st.session_state.latest_code = code_data
                            
#                             # Instantly overwrite the right screen with the Terraform Code
#                             with live_viewport.container():
#                                 st.info("👀 **Focus Mode:** Generating Terraform...")
#                                 with st.container(height=500):
#                                     for filename, content in code_data.items():
#                                         st.markdown(f"### 📄 `{filename}`")
#                                         clean_content = content.replace("\\n", "\n").replace("\\t", "  ")
#                                         st.code(clean_content, language="hcl", line_numbers=True)
                                    
#                         # --- 4. VALIDATOR LOGS ---
#                         elif "validation_agent" in chunk:
#                             val_data = chunk["validation_agent"]
#                             if val_data.get("validation_passed"):
#                                 status.write("✅ **Validation Agent** verified code syntax successfully.")
#                             else:
#                                 err = val_data.get('validation_errors', '')
#                                 status.write(f"⚠️ **Validation Agent** caught syntax anomalies! Routing back for fixing...")
#                                 status.write(f"```\n{err}\n```")
                
#                 status.update(label="Execution Complete!", state="complete", expanded=False)
                
#                 # Unlock streaming mode to bring the tabs back, and refresh the page!
#                 st.session_state.is_streaming = False
#                 st.rerun() 
                
#             except Exception as e:
#                 st.session_state.is_streaming = False
#                 status.update(label="Execution Aborted", state="error")
#                 st.error(f"Failed to process graph stream workflow: {e}")

import streamlit as st
import requests
import json

st.set_page_config(layout="wide", page_title="AI Platform Assistant")
st.title("Infra AI Agent")


# Initialize session state for messages and streaming cache
if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_streaming" not in st.session_state:
    st.session_state.is_streaming = False



# --- STEP 1: DEFINE LAYOUT COLUMNS ---
chat_col, output_col = st.columns([1, 1])



# --- STEP 2: INITIALIZE THE LIVE VIEWPORT ---
with output_col:

    st.subheader("Generated Infrastructure Deliverables")

    live_viewport = st.empty()



# --- STEP 3: RENDER HISTORICAL TABS (ONLY WHEN NOT STREAMING) ---

if not st.session_state.is_streaming and "latest_spec" in st.session_state:

    with live_viewport.container():

        tab1, tab2, tab3 = st.tabs(
            [
                "1. Extracted Spec",
                "2. Architecture Plan",
                "3. Terraform Code"
            ]
        )


        with tab1:

            st.json(
                st.session_state.latest_spec
            )


        with tab2:

            plan_data = st.session_state.latest_plan

            if isinstance(plan_data, list) and len(plan_data) > 0 and isinstance(plan_data[0], dict):

                plan_data = plan_data[0].get(
                    "text",
                    str(plan_data)
                )

            st.markdown(plan_data)



        with tab3:

            with st.container(height=500):

                for filename, content in st.session_state.latest_code.items():

                    st.markdown(
                        f"### 📄 `{filename}`"
                    )

                    clean_content = (
                        content
                        .replace("\\n", "\n")
                        .replace("\\t", "  ")
                    )

                    st.code(
                        clean_content,
                        language="hcl",
                        line_numbers=True
                    )




# --- STEP 4: CHAT CONVERSATION PROCESSING INTERFACE ---

with chat_col:

    st.subheader("Conversation")


    # Display previous messages

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.write(msg["content"])




    # Process new prompt inputs

    if prompt := st.chat_input(
        "E.g., Build an Azure environment with isolated networks..."
    ):


        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )


        st.session_state.is_streaming = True


        with st.chat_message("user"):

            st.write(prompt)



        with st.status(
            "🧠 Agents are thinking...",
            expanded=True
        ) as status:


            try:


                response = requests.post(

                    "http://localhost:8000/stream",

                    json={
                        "prompt": prompt
                    },

                    stream=True

                )



                # ==============================
                # STREAM RESPONSE HANDLING
                # ==============================

                for line in response.iter_lines():


                    if line:


                        chunk = json.loads(
                            line.decode("utf-8")
                        )



                        # =================================
                        # SECURITY GUARDRAIL RESPONSE
                        # =================================

                        if chunk.get("status") == "blocked":


                            status.update(

                                label="🚫 Request Blocked",

                                state="error",

                                expanded=True

                            )


                            st.error(
                                "🚫 Security Violation Detected"
                            )


                            st.warning(
                                chunk.get(
                                    "message",
                                    "Your request cannot be processed."
                                )
                            )


                            st.write(
                                "Detected:",
                                chunk.get(
                                    "reason",
                                    []
                                )
                            )


                            st.session_state.is_streaming = False


                            st.stop()



                        # =================================
                        # 1. INTENT PARSER
                        # =================================


                        if "intent_parser" in chunk:


                            status.write(
                                "✅ **Intent Parser** extracted requirements."
                            )


                            spec_data = chunk[
                                "intent_parser"
                            ].get(
                                "project_spec",
                                {}
                            )


                            st.session_state.latest_spec = spec_data



                            with live_viewport.container():

                                st.info(
                                    "👀 **Focus Mode:** Extracting Specification..."
                                )

                                st.json(
                                    spec_data
                                )





                        # =================================
                        # 2. ARCHITECTURE PLANNER
                        # =================================


                        elif "architecture_planner" in chunk:


                            status.write(
                                "✅ **Architecture Planner** designed the topology."
                            )


                            plan_data = chunk[
                                "architecture_planner"
                            ].get(
                                "architecture_plan",
                                ""
                            )


                            st.session_state.latest_plan = plan_data



                            if isinstance(plan_data, list) and len(plan_data) > 0 and isinstance(plan_data[0], dict):

                                plan_data = plan_data[0].get(
                                    "text",
                                    str(plan_data)
                                )



                            with live_viewport.container():

                                st.info(
                                    "👀 **Focus Mode:** Drafting Architecture Plan..."
                                )

                                st.markdown(
                                    plan_data
                                )





                        # =================================
                        # 3. IAC GENERATOR
                        # =================================


                        elif "iac_generator" in chunk:


                            status.write(
                                "✅ **IaC Generator** wrote the Terraform code."
                            )


                            code_data = chunk[
                                "iac_generator"
                            ].get(
                                "generated_code",
                                {}
                            )


                            st.session_state.latest_code = code_data



                            with live_viewport.container():


                                st.info(
                                    "👀 **Focus Mode:** Generating Terraform..."
                                )


                                with st.container(height=500):


                                    for filename, content in code_data.items():


                                        st.markdown(
                                            f"### 📄 `{filename}`"
                                        )


                                        clean_content = (
                                            content
                                            .replace("\\n","\n")
                                            .replace("\\t","  ")
                                        )


                                        st.code(
                                            clean_content,
                                            language="hcl",
                                            line_numbers=True
                                        )





                        # =================================
                        # 4. VALIDATOR
                        # =================================


                        elif "validation_agent" in chunk:


                            val_data = chunk[
                                "validation_agent"
                            ]


                            if val_data.get(
                                "validation_passed"
                            ):


                                status.write(
                                    "✅ **Validation Agent** verified code syntax successfully."
                                )


                            else:


                                err = val_data.get(
                                    "validation_errors",
                                    ""
                                )


                                status.write(
                                    "⚠️ **Validation Agent** caught syntax anomalies! Routing back for fixing..."
                                )


                                status.write(
                                    f"```\n{err}\n```"
                                )



                status.update(

                    label="Execution Complete!",

                    state="complete",

                    expanded=False

                )


                st.session_state.is_streaming = False

                st.rerun()



            except Exception as e:


                st.session_state.is_streaming = False


                status.update(

                    label="Execution Aborted",

                    state="error"

                )


                st.error(
                    f"Failed to process graph stream workflow: {e}"
                )