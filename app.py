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
                    project_plan=message.get("project_plan", {}),
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

    # -----------------------------------------
    # Store user message
    # -----------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        render_user_prompt(prompt)

    # -----------------------------------------
    # Assistant
    # -----------------------------------------

    with st.chat_message("assistant"):

        status = st.empty()

        try:

            response = stream_chat(
                prompt,
                st.session_state.thread_id,
            )

            final_output = None

            # -------------------------------------
            # Backend event stream
            # -------------------------------------

            for line in response.iter_lines():

                if not line:
                    continue

                event = json.loads(
                    line.decode("utf-8")
                )

                # Status event
                if event.get("type") == "status":

                    status.info(
                        event.get(
                            "message",
                            "Working..."
                        )
                    )

                # Clarification
                elif event.get("type") == "interrupt":

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": event["message"],
                        }
                    )

                    status.empty()

                    refresh_projects()
                    refresh_history()

                    st.rerun()

                # Final output
                elif event.get("type") == "complete":

                    final_output = event.get(
                        "output",
                        {}
                    )

                    if event.get("success"):

                        status.success(
                            "✅ Infrastructure generated "
                            "and validated successfully."
                        )

                    else:

                        status.error(
                            "❌ Infrastructure generation "
                            "could not be completed."
                        )

            # -------------------------------------
            # Final result
            # -------------------------------------

            if final_output:

                final_spec = final_output.get(
                    "project_spec",
                    {}
                )

                final_srs = final_output.get(
                    "srs",
                    ""
                )

                final_plan = final_output.get(
                    "architecture",
                    ""
                )

                final_project_plan = final_output.get(
                    "project_plan",
                    {}
                )

                final_code = final_output.get(
                    "terraform",
                    {}
                )

                summary = (
                    "✅ **Infrastructure generated successfully.**\n\n"
                    "Your infrastructure has been analyzed, planned, "
                    "generated and validated successfully.\n\n"
                    "Use the buttons below to inspect each artifact."
                )

                msg_id = len(
                    st.session_state.messages
                )

                render_assistant_output(
                    msg_id=msg_id,
                    summary=summary,
                    spec=final_spec,
                    srs=final_srs,
                    plan=final_plan,
                    project_plan=final_project_plan,
                    code=final_code,
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "summary": summary,
                        "spec": final_spec,
                        "srs": final_srs,
                        "plan": final_plan,
                        "project_plan": final_project_plan,
                        "code": final_code,
                    }
                )

                refresh_projects()
                refresh_history()

                st.toast(
                    "Infrastructure generated successfully 🚀",
                    icon="✅",
                )

            else:

                st.warning(
                    "The workflow completed, but no final "
                    "output was returned."
                )

        except Exception as e:

            status.error(
                f"❌ {str(e)}"
            )

            st.stop()
