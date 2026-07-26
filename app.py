import json
import streamlit as st

from styles import CUSTOM_CSS

from state import (
    init_session_state,
)

from sidebar import (
    render_sidebar,
)

from renderer import (
    render_user_prompt,
    render_assistant_output,
)

from api import (
    stream_chat,
    refresh_projects,
    refresh_history,
)

# -----------------------------------------------------
# Page Config
# -----------------------------------------------------

st.set_page_config(
    page_title="Infra AI Agent",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------
# Initialize Session
# -----------------------------------------------------

init_session_state()

# -----------------------------------------------------
# Sidebar
# -----------------------------------------------------

render_sidebar()

# -----------------------------------------------------
# Main Page
# -----------------------------------------------------

st.title("🚀 Infra AI Agent")

st.caption(
    f"Workspace ID: `{st.session_state.thread_id}`"
)

st.divider()

# -----------------------------------------------------
# Render Existing Conversation
# -----------------------------------------------------

for idx, message in enumerate(st.session_state.messages):

    if message["role"] == "user":

        with st.chat_message("user"):

            render_user_prompt(
                message["content"]
            )

    elif message["role"] == "assistant":

        with st.chat_message("assistant"):
            if "content" in message:

                st.markdown(message["content"])

            else:

                render_assistant_output(
                    msg_id=idx,
                    summary=message.get("summary", ""),
                    spec=message.get("spec", {}),
                    srs=message.get("srs", ""),
                    plan=message.get("plan", ""),
                    code=message.get("code", {}),
                )

# -----------------------------------------------------
# Chat Input
# -----------------------------------------------------

placeholder = "Describe the infrastructure you want..."

if (
    st.session_state.messages
    and st.session_state.messages[-1]["role"] == "assistant"
    and "content" in st.session_state.messages[-1]
):
    placeholder = "Answer the clarification question..."

if prompt := st.chat_input(placeholder):

    # -------------------------------
    # Store User Message
    # -------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        render_user_prompt(prompt)

    # -------------------------------
    # Assistant
    # -------------------------------

    with st.chat_message("assistant"):

        status = st.empty()

        status.info("🧠 Parsing requirements...")

        final_spec = {}
        final_plan = ""
        final_srs = ""
        final_code = {}

        try:

            response = stream_chat(
                prompt,
                st.session_state.thread_id,
            )

            for line in response.iter_lines():

                if not line:
                    continue

                event = json.loads(
                    line.decode("utf-8")
                )

                # -------------------------
                # Intent Parser
                # -------------------------

                if "intent_parser" in event:

                    status.info(
                        "📝 Building Software Requirements..."
                    )

                    parser = event["intent_parser"]

                    final_spec = parser.get(
                        "project_spec",
                        {},
                    )

                # -------------------------
                # SRS Generator
                # -------------------------

                if "srs_generator" in event:

                    status.info(
                        "📝 Generating SRS Document..."
                    )

                    srs = event["srs_generator"]

                    final_srs = srs.get(
                        "srs_document",
                        "",
                    )

                # -------------------------
                # Interrupt
                # -------------------------
                if event.get("type") == "interrupt":
                    print(event)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": event["message"],
                    })

                    status.empty()

                    refresh_projects()
                    refresh_history()

                    st.rerun()

                # -------------------------
                # Architecture Planner
                # -------------------------

                elif "architecture_planner" in event:

                    status.info(
                        "🏗️ Designing Architecture..."
                    )

                    planner = event[
                        "architecture_planner"
                    ]

                    final_plan = planner.get(
                        "architecture_plan",
                        "",
                    )

                # -------------------------
                # Terraform Generator
                # -------------------------

                elif "iac_generator" in event:

                    status.info(
                        "💻 Generating Terraform..."
                    )

                    generator = event[
                        "iac_generator"
                    ]

                    final_code = generator.get(
                        "generated_code",
                        {},
                    )

                # -------------------------
                # Validator
                # -------------------------

                elif "validation_agent" in event:

                    validator = event[
                        "validation_agent"
                    ]

                    if validator.get(
                        "validation_passed"
                    ):

                        status.success(
                            "✅ Validation Passed"
                        )

                    else:

                        attempt = validator.get(
                            "validation_attempts",
                            1,
                        )

                        status.warning(
                            f"⚠ Validation failed. "
                            f"Retrying ({attempt}/3)..."
                        )

            status.empty()

        except Exception as e:

            status.error(str(e))

            st.stop()



            # -------------------------------------------------
        # Final Assistant Response
        # -------------------------------------------------

        if final_code:

            summary = (
                "✅ **Infrastructure generated successfully.**\n\n"
                "Your infrastructure has been analyzed, planned, "
                "converted into Terraform and validated successfully.\n\n"
                "Use the buttons below to inspect each artifact."
            )

            msg_id = len(st.session_state.messages)

            render_assistant_output(
                msg_id=msg_id,
                summary=summary,
                spec=final_spec,
                srs=final_srs,
                plan=final_plan,
                code=final_code,
            )

            assistant_message = {
                "role": "assistant",
                "summary": summary,
                "spec": final_spec,
                "srs": final_srs,
                "plan": final_plan,
                "code": final_code,
            }

            st.session_state.messages.append(
                assistant_message
            )

            # -----------------------------------------
            # Refresh cached backend data
            # -----------------------------------------

            refresh_projects()

            refresh_history()

            st.toast(
                "Infrastructure generated successfully 🚀",
                icon="✅",
            )

        else:

            st.warning(
                "The workflow completed, but no Terraform "
                "files were generated."
            )