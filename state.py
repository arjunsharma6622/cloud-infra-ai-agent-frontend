import streamlit as st
import uuid
import json


def init_session_state():
    """Initialize all session state variables."""

    defaults = {
        "thread_id": str(uuid.uuid4()),
        "messages": [],
        "projects": [],
        "project_cache": {},
        "active_project": None,
        "is_streaming": False,
        "deployment": None,
        "deployment_started": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def new_project():
    """Reset UI for a brand-new infrastructure project."""

    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.active_project = st.session_state.thread_id
    st.session_state.is_streaming = False


def load_project(thread_id: str, history: dict):
    """Load a project returned from the backend into session state."""

    st.session_state.thread_id = thread_id
    st.session_state.active_project = thread_id

    messages = []

    for msg in history.get("messages", []):

        message = {
            "role": msg["role"],
            "message_type": msg["message_type"]
        }

        if msg["message_type"] == "final_output":
            data = json.loads(msg["content"])

            message.update(
                {
                    "summary": "✅ **Infrastructure recovered from history.**",
                    "spec": data.get("spec", {}),
                    "srs": data.get("srs", ""),
                    "plan": data.get("architecture", ""),
                    "code": data.get("terraform", {}),
                }
            )
        else:
            message["content"] = msg["content"]

        messages.append(message)

    st.session_state.messages = messages

    # Cache it so we don't fetch it again
    st.session_state.project_cache[thread_id] = history